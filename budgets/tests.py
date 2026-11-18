
from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import (
    BudgetPlan,
    BudgetItem,
    BudgetReview,
    ReminderPreference,
)

from .services import calculate_budget_summary


class BudgetModelTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="budget_tester",
            password="test-password-123",
        )

        self.plan = BudgetPlan.objects.create(
            user=self.user,
            title="November Budget",
            budget_month=date(2026, 11, 1),
        )

    def test_budget_belongs_to_user(self):
        self.assertEqual(self.plan.user, self.user)

    def test_budget_starts_as_draft(self):
        self.assertEqual(
            self.plan.status,
            BudgetPlan.Status.DRAFT,
        )

    def test_budget_month_must_start_on_first(self):
        self.plan.budget_month = date(2026, 11, 15)

        with self.assertRaises(ValidationError):
            self.plan.full_clean()

    def test_budget_item_tracks_planned_and_actual(self):
        item = BudgetItem.objects.create(
            budget_plan=self.plan,
            description="Groceries",
            item_type=BudgetItem.ItemType.EXPENSE,
            planned_amount=Decimal("1200.00"),
            actual_amount=Decimal("1350.00"),
            is_priority=True,
        )

        self.assertEqual(
            item.planned_amount,
            Decimal("1200.00"),
        )
        self.assertEqual(
            item.actual_amount,
            Decimal("1350.00"),
        )

    def test_actual_amount_can_be_unrecorded(self):
        item = BudgetItem.objects.create(
            budget_plan=self.plan,
            description="Transport",
            item_type=BudgetItem.ItemType.EXPENSE,
            planned_amount=Decimal("800.00"),
        )

        self.assertIsNone(item.actual_amount)

    def test_negative_planned_amount_is_invalid(self):
        item = BudgetItem(
            budget_plan=self.plan,
            description="Invalid expense",
            item_type=BudgetItem.ItemType.EXPENSE,
            planned_amount=Decimal("-100.00"),
        )

        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_review_requires_user_success_decision(self):
        review = BudgetReview.objects.create(
            budget_plan=self.plan,
            within_expense_limit=True,
            priorities_paid=True,
            positive_closing_balance=True,
            marked_successful=False,
        )

        self.assertFalse(review.marked_successful)

    def test_default_reminder_day_is_fifteenth(self):
        preference = ReminderPreference.objects.create(
            user=self.user,
        )

        self.assertEqual(preference.reminder_day, 15)
        self.assertTrue(preference.enabled)

    def test_deleting_budget_deletes_related_records(self):
        item = BudgetItem.objects.create(
            budget_plan=self.plan,
            description="Rent",
            item_type=BudgetItem.ItemType.EXPENSE,
            planned_amount=Decimal("2000.00"),
        )

        review = BudgetReview.objects.create(
            budget_plan=self.plan,
        )

        item_id = item.id
        review_id = review.id

        self.plan.delete()

        self.assertFalse(
            BudgetItem.objects.filter(id=item_id).exists()
        )
        self.assertFalse(
            BudgetReview.objects.filter(id=review_id).exists()
        )


class BudgetSummaryTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="summary_tester",
            password="test-password-123",
        )

        self.plan = BudgetPlan.objects.create(
            user=self.user,
            title="November Budget",
            budget_month=date(2026, 11, 1),
        )

        self.income = BudgetItem.objects.create(
            budget_plan=self.plan,
            description="Salary",
            item_type=BudgetItem.ItemType.INCOME,
            planned_amount=Decimal("8000.00"),
            actual_amount=Decimal("8000.00"),
        )

        self.rent = BudgetItem.objects.create(
            budget_plan=self.plan,
            description="Rent",
            item_type=BudgetItem.ItemType.EXPENSE,
            planned_amount=Decimal("2000.00"),
            actual_amount=Decimal("2000.00"),
            is_priority=True,
            is_paid=True,
        )

        self.groceries = BudgetItem.objects.create(
            budget_plan=self.plan,
            description="Groceries",
            item_type=BudgetItem.ItemType.EXPENSE,
            planned_amount=Decimal("3500.00"),
            actual_amount=Decimal("3850.00"),
        )

    def test_complete_budget_calculations(self):
        summary = calculate_budget_summary(self.plan)

        self.assertEqual(
            summary["planned_income"],
            Decimal("8000.00"),
        )
        self.assertEqual(
            summary["planned_expenses"],
            Decimal("5500.00"),
        )
        self.assertEqual(
            summary["planned_balance"],
            Decimal("2500.00"),
        )
        self.assertEqual(
            summary["actual_balance"],
            Decimal("2150.00"),
        )
        self.assertEqual(
            summary["expense_variance"],
            Decimal("-350.00"),
        )

        self.assertFalse(summary["within_expense_limit"])
        self.assertTrue(summary["priorities_paid"])
        self.assertTrue(summary["positive_closing_balance"])
        self.assertTrue(summary["ready_for_review"])

    def test_missing_actual_amount_is_not_zero(self):
        self.groceries.actual_amount = None
        self.groceries.save()

        summary = calculate_budget_summary(self.plan)

        self.assertEqual(
            summary["recorded_expenses"],
            Decimal("2000.00"),
        )
        self.assertIsNone(summary["actual_balance"])
        self.assertIsNone(summary["expense_variance"])
        self.assertIsNone(summary["within_expense_limit"])
        self.assertIsNone(summary["positive_closing_balance"])
        self.assertFalse(summary["ready_for_review"])

    def test_zero_actual_amount_counts_as_recorded(self):
        self.groceries.actual_amount = Decimal("0.00")
        self.groceries.save()

        summary = calculate_budget_summary(self.plan)

        self.assertTrue(summary["ready_for_review"])
        self.assertTrue(summary["within_expense_limit"])
        self.assertEqual(
            summary["actual_balance"],
            Decimal("6000.00"),
        )

    def test_unpaid_priority_fails_priority_check(self):
        self.rent.is_paid = False
        self.rent.save()

        summary = calculate_budget_summary(self.plan)

        self.assertFalse(summary["priorities_paid"])
        self.assertTrue(summary["ready_for_review"])

    def test_calculations_do_not_change_user_decision(self):
        review = BudgetReview.objects.create(
            budget_plan=self.plan,
            marked_successful=False,
        )

        calculate_budget_summary(self.plan)

        review.refresh_from_db()
        self.assertFalse(review.marked_successful)

    def test_empty_budget_is_not_ready_for_review(self):
        empty_plan = BudgetPlan.objects.create(
            user=self.user,
            title="December Budget",
            budget_month=date(2026, 12, 1),
        )

        summary = calculate_budget_summary(empty_plan)

        self.assertFalse(summary["ready_for_review"])
        self.assertIsNone(summary["actual_balance"])
