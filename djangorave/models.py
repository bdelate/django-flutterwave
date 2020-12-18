# stdlib import

# django imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

# 3rd party imports

# project imports

UserModel = get_user_model()


class DRPlanModel(models.Model):
    """Represents either a Plan or OnceOff payment type"""

    description = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    payment_plan = models.PositiveIntegerField(unique=True, blank=True, null=True)
    currency = models.CharField(max_length=3, default="USD")
    custom_logo = models.URLField(max_length=500, blank=True, null=True)
    custom_title = models.CharField(max_length=200, blank=True, null=True)
    pay_button_text = models.CharField(max_length=100, default="Sign Up")
    payment_options = models.CharField(max_length=100, default="card")
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

    def __str__(self):
        return self.description


class DRTransactionModel(models.Model):
    """Represents a transaction for a specific payment type and user"""

    plan = models.ForeignKey(
        to=DRPlanModel, related_name="dr_transactions", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=UserModel, related_name="dr_transactions", on_delete=models.CASCADE
    )
    created_datetime = models.DateTimeField(auto_now_add=True)
    tx_ref = models.CharField(max_length=100)
    flw_ref = models.CharField(max_length=100)
    device_fingerprint = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    currency = models.CharField(max_length=3)
    charged_amount = models.DecimalField(decimal_places=2, max_digits=9)
    app_fee = models.DecimalField(decimal_places=2, max_digits=9)
    merchant_fee = models.DecimalField(decimal_places=2, max_digits=9)
    processor_response = models.CharField(max_length=100)
    auth_model = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    narration = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50)
    created_at = models.CharField(max_length=100)
    account_id = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return self.tx_ref
