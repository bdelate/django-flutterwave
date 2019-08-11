# stdlib import

# django imports
from django.contrib import admin

# project imports
from djangorave.models import PaymentMethodModel, TransactionModel

# project imports


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("description", "amount", "currency")


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("reference", "amount")


admin.site.register(PaymentMethodModel, PaymentMethodAdmin)
admin.site.register(TransactionModel, TransactionAdmin)
