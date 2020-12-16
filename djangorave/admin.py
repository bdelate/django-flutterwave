# stdlib import

# django imports
from django.contrib import admin

# project imports
from djangorave.models import DRPaymentTypeModel, DRTransactionModel

# project imports


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ("description", "amount", "payment_plan")
    search_fields = ("description",)
    readonly_fields = ("created_datetime",)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "payment_type", "reference", "amount", "created_datetime")
    search_fields = ("user__username", "payment_type__description", "reference")
    readonly_fields = ("created_datetime",)


admin.site.register(DRPaymentTypeModel, PaymentTypeAdmin)
admin.site.register(DRTransactionModel, TransactionAdmin)
