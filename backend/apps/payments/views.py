"""
Stripe Checkout + webhook — test keys se kaam karega.
"""
import stripe
from django.conf import settings
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from apps.courses.models import Enrollment

from .models import Coupon, Invoice, Order, OrderStatus, SubscriptionPlan
from .serializers import CheckoutSerializer, OrderSerializer, SubscriptionPlanSerializer


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = CheckoutSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        course = ser.validated_data["course"]
        coupon_code = (ser.validated_data.get("coupon_code") or "").strip()
        amount = course.price_cents
        coupon_obj = None
        if coupon_code:
            c = Coupon.objects.filter(code__iexact=coupon_code, active=True).first()
            if c:
                coupon_obj = c
                if c.percent_off:
                    amount = int(amount * (100 - c.percent_off) / 100)
                elif c.amount_off_cents:
                    amount = max(0, amount - c.amount_off_cents)
        if not settings.STRIPE_SECRET_KEY:
            order = Order.objects.create(
                user=request.user,
                course=course,
                coupon=coupon_obj,
                amount_cents=amount,
                status=OrderStatus.PAID,
            )
            Enrollment.objects.get_or_create(user=request.user, course=course)
            Invoice.objects.create(order=order)
            return Response(
                {
                    "detail": "Stripe key missing — demo mode mein order paid mark.",
                    "order": OrderSerializer(order).data,
                }
            )
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = Order.objects.create(
            user=request.user,
            course=course,
            coupon=coupon_obj,
            amount_cents=amount,
            status=OrderStatus.PENDING,
        )
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": amount,
                        "product_data": {"name": course.title},
                    },
                    "quantity": 1,
                }
            ],
            success_url=f"{settings.FRONTEND_URL}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.FRONTEND_URL}/checkout/cancel",
            metadata={"order_id": str(order.id)},
        )
        order.stripe_session_id = session.id
        order.save(update_fields=["stripe_session_id"])
        return Response({"checkout_url": session.url, "order_id": order.id})


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
        if not settings.STRIPE_WEBHOOK_SECRET or not settings.STRIPE_SECRET_KEY:
            return Response({"detail": "Stripe webhook/secret set nahi"}, status=400)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        except ValueError:
            return Response(status=400)
        except stripe.error.SignatureVerificationError:
            return Response(status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            order_id = session.get("metadata", {}).get("order_id")
            if order_id:
                order = Order.objects.filter(id=order_id).first()
                if order and order.status == OrderStatus.PENDING:
                    order.status = OrderStatus.PAID
                    order.stripe_payment_intent = session.get("payment_intent") or ""
                    order.save()
                    Enrollment.objects.get_or_create(user=order.user, course=order.course)
                    Invoice.objects.get_or_create(order=order)
                    if order.coupon_id:
                        Coupon.objects.filter(pk=order.coupon_id).update(times_redeemed=F("times_redeemed") + 1)
        return Response({"received": True})


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("course")


class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = SubscriptionPlan.objects.filter(active=True)
    serializer_class = SubscriptionPlanSerializer


class RefundRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        order = Order.objects.filter(id=order_id, user=request.user).first()
        if not order:
            return Response({"detail": "Order nahi mila"}, status=404)
        if order.status != OrderStatus.PAID:
            return Response({"detail": "Refund sirf paid orders par"}, status=400)
        if not settings.STRIPE_SECRET_KEY or not order.stripe_payment_intent:
            order.status = OrderStatus.REFUNDED
            order.save(update_fields=["status"])
            return Response({"detail": "Demo refund — status refunded"})
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.Refund.create(payment_intent=order.stripe_payment_intent)
        order.status = OrderStatus.REFUNDED
        order.save(update_fields=["status"])
        return Response({"detail": "Refund initiated"})
