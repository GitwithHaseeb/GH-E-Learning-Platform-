from rest_framework import serializers

from apps.courses.models import Course, CourseStatus, PricingType

from .models import Coupon, Order, OrderStatus, SubscriptionPlan


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ("code", "percent_off", "amount_off_cents", "active")


class CheckoutSerializer(serializers.Serializer):
    course_slug = serializers.SlugField()
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        slug = attrs["course_slug"]
        course = Course.objects.filter(slug=slug).first()
        if not course:
            raise serializers.ValidationError({"course_slug": "Course nahi mila."})
        if course.status != CourseStatus.PUBLISHED:
            raise serializers.ValidationError({"course_slug": "Course publish nahi hai."})
        if course.pricing == PricingType.FREE:
            raise serializers.ValidationError({"course_slug": "Yeh course free hai — seedha enroll karein."})
        attrs["course"] = course
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "course",
            "course_title",
            "amount_cents",
            "currency",
            "status",
            "stripe_session_id",
            "created_at",
        )
        read_only_fields = fields


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ("id", "name", "interval", "amount_cents", "active", "stripe_price_id")
