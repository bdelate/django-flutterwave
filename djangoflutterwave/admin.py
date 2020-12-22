# stdlib import

# django imports
from django.contrib import admin

# project imports
from djangoflutterwave.models import FlwPlanModel, FlwTransactionModel

# project imports


class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "flw_plan_id", "interval")
    search_fields = ("name",)
    readonly_fields = ("created_datetime",)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "status", "tx_ref", "amount", "created_at")
    search_fields = ("user__username", "plan__name", "tx_ref")
    readonly_fields = ("created_datetime",)


admin.site.register(FlwPlanModel, PlanAdmin)
admin.site.register(FlwTransactionModel, TransactionAdmin)
