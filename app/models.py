from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone


class Transaction(models.Model):

    TRANSACTION_TYPES = (
        ('deposit', 'deposit'),
        ('withdrawal', 'withdrawal'),
    )

    CATEGORY_TYPES = (
        ('groceries', 'groceries'),
        ('utilities', 'utilities'),
        ('transfers', 'transfers'),
        ('tax', 'tax'),
        ('travel', 'travel'),
        ('loan', 'loan'),
    )

    user = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE)

    transaction_type = models.CharField(
        max_length=200,
        null=False,
        choices=TRANSACTION_TYPES)

    category_type = models.CharField(
        max_length=200,
        null=True,
        choices=CATEGORY_TYPES)

    amount = models.DecimalField(
        max_digits=100,
        null=False,
        decimal_places=2)

    timestamp = models.DateTimeField(
        default=timezone.now,
        null=False)

    def __str__(self):
        return self.user.__str__()