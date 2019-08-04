# stdlib import

# django imports
from django.contrib import admin

# project imports
from djangorave.models import PlanModel, OnceOffModel

# project imports


class PaymentBaseAdmin(admin.ModelAdmin):
    list_display = ("description", "amount", "currency")


class PlanAdmin(PaymentBaseAdmin):
    list_display = ("payment_plan",) + PaymentBaseAdmin.list_display


class OnceOffAdmin(PaymentBaseAdmin):
    pass


admin.site.register(PlanModel, PlanAdmin)
admin.site.register(OnceOffModel, OnceOffAdmin)
