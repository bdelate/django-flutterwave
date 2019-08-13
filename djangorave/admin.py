# stdlib import

# django imports
from django.contrib import admin

# project imports
from djangorave.models import PaymentTypeModel, TransactionModel

# project imports


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ("description", "amount", "currency")


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("reference", "amount")


admin.site.register(PaymentTypeModel, PaymentTypeAdmin)
admin.site.register(TransactionModel, TransactionAdmin)
