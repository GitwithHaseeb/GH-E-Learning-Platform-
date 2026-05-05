from django.contrib import admin

from .models import Coupon, InstructorPayout, Invoice, Order, SubscriptionPlan, UserSubscription


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "percent_off", "amount_off_cents", "active", "times_redeemed")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "amount_cents", "status", "created_at")
    list_filter = ("status",)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "interval", "amount_cents", "active")


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "active", "current_period_end")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "order", "created_at")


@admin.register(InstructorPayout)
class InstructorPayoutAdmin(admin.ModelAdmin):
    list_display = ("instructor", "amount_cents", "status", "period_start", "period_end")
