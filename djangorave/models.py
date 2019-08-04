# stdlib import

# django imports
from django.db import models

# 3rd party imports

# project imports


class PaymentBaseModel(models.Model):
    """Represents the base data required for either a Plan or OnceOff payment
    method"""

    description = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    currency = models.CharField(max_length=3, default="USD")
    custom_logo = models.URLField(max_length=500, blank=True, null=True)
    custom_title = models.CharField(max_length=200, blank=True, null=True)
    pay_button_text = models.CharField(max_length=100, default="Sign Up")
    payment_options = models.CharField(max_length=100, default="card")

    class Meta:
        abstract = True

    def __str__(self):
        return self.description


class PlanModel(PaymentBaseModel):
    """Represents a recurring payment plan

    payment_plan: Rave plan ID
    """

    payment_plan = models.PositiveIntegerField(unique=True)

    class Meta(PaymentBaseModel.Meta):
        verbose_name = "Plan"
        verbose_name_plural = "Plans"


class OnceOffModel(PaymentBaseModel):
    """Represents a once off payment"""

    class Meta(PaymentBaseModel.Meta):
        verbose_name = "Once Off Payment Option"
        verbose_name_plural = "Once Off Payment Options"
