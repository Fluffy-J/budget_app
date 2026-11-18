
from decimal import Decimal

from .models import BudgetItem


ZERO = Decimal("0.00")


def calculate_budget_summary(budget_plan):
    """
    Calculate planned and actual budget totals.

    Missing actual amounts remain unrecorded,
    rather than being treated as zero.
    """

    items = list(budget_plan.items.all())

    income_items = [
        item for item in items
        if item.item_type == BudgetItem.ItemType.INCOME
    ]

    expense_items = [
        item for item in items
        if item.item_type == BudgetItem.ItemType.EXPENSE
    ]

    # Planned amounts
    planned_income = sum(
        (item.planned_amount for item in income_items),
        ZERO,
    )

    planned_expenses = sum(
        (item.planned_amount for item in expense_items),
        ZERO,
    )

    planned_balance = planned_income - planned_expenses

    # Actual amounts recorded so far
    recorded_income = sum(
        (
            item.actual_amount
            for item in income_items
            if item.actual_amount is not None
        ),
        ZERO,
    )

    recorded_expenses = sum(
        (
            item.actual_amount
            for item in expense_items
            if item.actual_amount is not None
        ),
        ZERO,
    )

    # Completeness checks
    income_complete = bool(income_items) and all(
        item.actual_amount is not None
        for item in income_items
    )

    expenses_complete = bool(expense_items) and all(
        item.actual_amount is not None
        for item in expense_items
    )

    ready_for_review = income_complete and expenses_complete

    # Actual net balance is only final when
    # all income and expenses have been recorded.
    actual_balance = (
        recorded_income - recorded_expenses
        if ready_for_review
        else None
    )

    expense_variance = (
        planned_expenses - recorded_expenses
        if expenses_complete
        else None
    )

    # Budget success criteria
    within_expense_limit = (
        recorded_expenses <= planned_expenses
        if expenses_complete
        else None
    )

    priority_items = [
        item for item in expense_items
        if item.is_priority
    ]

    priorities_paid = all(
        item.is_paid and item.actual_amount is not None
        for item in priority_items
    )

    positive_closing_balance = (
        actual_balance > ZERO
        if ready_for_review
        else None
    )

    return {
        "planned_income": planned_income,
        "planned_expenses": planned_expenses,
        "planned_balance": planned_balance,
        "recorded_income": recorded_income,
        "recorded_expenses": recorded_expenses,
        "actual_balance": actual_balance,
        "expense_variance": expense_variance,
        "income_complete": income_complete,
        "expenses_complete": expenses_complete,
        "ready_for_review": ready_for_review,
        "within_expense_limit": within_expense_limit,
        "priorities_paid": priorities_paid,
        "positive_closing_balance": positive_closing_balance,
    }