"""
Stripe orders, coupons, subscriptions, invoices, instructor payouts.
"""
import uuid

from django.conf import settings
from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class Coupon(models.Model):
    code = models.CharField(max_length=40, unique=True, db_index=True)
    percent_off = models.PositiveSmallIntegerField(default=0)
    amount_off_cents = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    max_redemptions = models.PositiveIntegerField(null=True, blank=True)
    times_redeemed = models.PositiveIntegerField(default=0)
    valid_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="orders")
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    amount_cents = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, default="usd")
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    stripe_session_id = models.CharField(max_length=255, blank=True)
    stripe_payment_intent = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["stripe_session_id"]),
        ]


class SubscriptionInterval(models.TextChoices):
    MONTHLY = "monthly", "Monthly"
    YEARLY = "yearly", "Yearly"


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=120)
    stripe_price_id = models.CharField(max_length=120, blank=True)
    interval = models.CharField(max_length=20, choices=SubscriptionInterval.choices)
    amount_cents = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.interval})"


class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    stripe_subscription_id = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    current_period_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["user", "active"])]


def _invoice_number():
    return str(uuid.uuid4()).replace("-", "")[:20]


class Invoice(models.Model):
    order = models.OneToOneField(Order, null=True, blank=True, on_delete=models.CASCADE, related_name="invoice")
    subscription = models.ForeignKey(
        UserSubscription, null=True, blank=True, on_delete=models.CASCADE, related_name="invoices"
    )
    number = models.CharField(max_length=40, unique=True, default=_invoice_number)
    pdf_file = models.FileField(upload_to="invoices/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PayoutStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"


class InstructorPayout(models.Model):
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payouts"
    )
    amount_cents = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=PayoutStatus.choices, default=PayoutStatus.PENDING)
    period_start = models.DateField()
    period_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
