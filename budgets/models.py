
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q


class BudgetPlan(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ACTIVE = "ACTIVE", "Active"
        ARCHIVED = "ARCHIVED", "Archived"

    public_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="budget_plans",
    )

    source_plan = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_plans",
    )

    title = models.CharField(max_length=150)
    budget_month = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-budget_month", "-created_at"]

    def clean(self):
        super().clean()

        if self.budget_month and self.budget_month.day != 1:
            raise ValidationError({
                "budget_month": "Use the first day of the month."
            })

        if self.source_plan_id and self.user_id:
            if self.source_plan.user_id != self.user_id:
                raise ValidationError({
                    "source_plan": "The source budget must belong to the same user."
                })

        if self.pk and self.source_plan_id == self.pk:
            raise ValidationError({
                "source_plan": "A budget cannot be its own source."
            })

    def __str__(self):
        return f"{self.title} ({self.budget_month:%B %Y})"


class BudgetItem(models.Model):
    class ItemType(models.TextChoices):
        INCOME = "INCOME", "Income"
        EXPENSE = "EXPENSE", "Expense"

    budget_plan = models.ForeignKey(
        BudgetPlan,
        on_delete=models.CASCADE,
        related_name="items",
    )

    description = models.CharField(max_length=200)

    item_type = models.CharField(
        max_length=10,
        choices=ItemType.choices,
    )

    planned_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    actual_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    is_priority = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(planned_amount__gte=0),
                name="budget_item_planned_nonnegative",
            ),
            models.CheckConstraint(
                condition=(
                    Q(actual_amount__gte=0)
                    | Q(actual_amount__isnull=True)
                ),
                name="budget_item_actual_nonnegative",
            ),
        ]

    def clean(self):
        super().clean()

        if self.item_type == self.ItemType.INCOME:
            if self.is_priority or self.is_paid:
                raise ValidationError(
                    "Priority and paid flags apply only to expenses."
                )

        if self.is_paid and self.actual_amount is None:
            raise ValidationError({
                "actual_amount": "Record the actual amount before marking an expense paid."
            })

    def __str__(self):
        return self.description


class BudgetReview(models.Model):
    budget_plan = models.OneToOneField(
        BudgetPlan,
        on_delete=models.CASCADE,
        related_name="review",
    )

    within_expense_limit = models.BooleanField(
        null=True,
        blank=True,
    )
    priorities_paid = models.BooleanField(
        null=True,
        blank=True,
    )
    positive_closing_balance = models.BooleanField(
        null=True,
        blank=True,
    )

    marked_successful = models.BooleanField(default=False)
    review_note = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review: {self.budget_plan.title}"


class ReminderPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reminder_preference",
    )

    reminder_day = models.PositiveSmallIntegerField(
        default=15,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(31),
        ],
    )

    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}: day {self.reminder_day}"