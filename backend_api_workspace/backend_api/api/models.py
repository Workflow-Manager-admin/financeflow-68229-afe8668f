from django.db import models
from django.contrib.auth.models import User


# PUBLIC_INTERFACE
class Category(models.Model):
    """
    Represents an expense category (e.g., Food, Transport, Utilities).
    """
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories',
        help_text="Owner of the category (the user who created it)."
    )

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('name', 'user')

    def __str__(self):
        return f"{self.name} ({self.user.username})"


# PUBLIC_INTERFACE
class Expense(models.Model):
    """
    Represents a financial expense event.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='expenses',
        help_text="Expense owner (who made this expense)."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='expenses',
        help_text="Category for this expense."
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Expense amount, up to 10 digits and 2 decimal places."
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional description of the expense."
    )
    date = models.DateField(
        help_text="Date that the expense occurred."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Time the expense was created (set automatically)."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Time the expense was last updated (set automatically)."
    )

    def __str__(self):
        cat_name = self.category.name if self.category else 'Uncategorized'
        return f"{self.user.username} - {cat_name}: {self.amount}"
