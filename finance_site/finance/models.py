from django.conf import settings
from django.db import models


class Category(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    name = models.CharField(max_length=100)
    is_income = models.BooleanField(default=False)

    class Meta:
        unique_together = ("owner", "name")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    KIND_CHOICES = [
        ("income", "Доход"),
        ("expense", "Расход"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    kind = models.CharField(max_length=7, choices=KIND_CHOICES)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.date} {self.kind} {self.amount}"
