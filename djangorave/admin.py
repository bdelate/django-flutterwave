# stdlib import

# django imports
from django.contrib import admin

# project imports
from djangorave.models import DRPlanModel, DRTransactionModel

# project imports


class PlanAdmin(admin.ModelAdmin):
    list_display = ("description", "amount", "payment_plan")
    search_fields = ("description",)
    readonly_fields = ("created_datetime",)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "tx_ref", "amount", "created_datetime")
    search_fields = ("user__username", "plan__description", "tx_ref")
    readonly_fields = ("created_datetime",)


admin.site.register(DRPlanModel, PlanAdmin)
admin.site.register(DRTransactionModel, TransactionAdmin)
