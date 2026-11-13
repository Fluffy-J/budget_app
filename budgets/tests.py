
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