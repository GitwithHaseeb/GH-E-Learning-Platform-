from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CreateCheckoutSessionView,
    OrderViewSet,
    RefundRequestView,
    StripeWebhookView,
    SubscriptionPlanViewSet,
)

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="payment-order")
router.register("subscription-plans", SubscriptionPlanViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("checkout/create/", CreateCheckoutSessionView.as_view(), name="checkout-create"),
    path("webhooks/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"),
    path("refund/", RefundRequestView.as_view(), name="refund-request"),
]
