# stdlib import

# django imports
from django.contrib.auth import get_user_model
from django.db import models

# 3rd party imports

# project imports

UserModel = get_user_model()


class FlwPlanModel(models.Model):
    """Represents either a Plan or OnceOff payment type"""

    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    BI_ANNUALLY = "bi_annually"
    YEARLY = "yearly"
    INTERVAL_CHOICES = (
        (HOURLY, "Hourly"),
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (MONTHLY, "Monthly"),
        (QUARTERLY, "Quarterly"),
        (BI_ANNUALLY, "Bi Annually"),
        (YEARLY, "Yearly"),
    )
    name = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    flw_plan_id = models.PositiveIntegerField(
        unique=True,
        blank=True,
        null=True,
        help_text="Flutterwave plan id. Only required if this is a subscription plan.",
    )
    interval = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        choices=INTERVAL_CHOICES,
        help_text="Payment frequency. Only required if this is a subscription plan.",
    )
    currency = models.CharField(max_length=3, default="USD")
    modal_logo_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL to logo image to be displayed on payment modal.",
    )
    modal_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Title to be displayed on payment modal.",
    )
    pay_button_text = models.CharField(
        max_length=100,
        default="Sign Up",
        help_text="Text used for button when displayed in a template.",
    )
    pay_button_css_classes = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="css classes to be applied to pay button in template.",
    )
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

    def __str__(self):
        return self.name


class FlwTransactionModel(models.Model):
    """Represents a transaction for a specific payment type and user"""

    plan = models.ForeignKey(
        to=FlwPlanModel, related_name="flw_transactions", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=UserModel, related_name="flw_transactions", on_delete=models.CASCADE
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
    created_at = models.DateTimeField(
        help_text="Created datetime received from Flutterwave"
    )
    account_id = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return self.tx_ref
