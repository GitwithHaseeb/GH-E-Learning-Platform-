import django_filters

from .models import Course, CourseLevel, PricingType


class CourseFilter(django_filters.FilterSet):
    """Listing filters — price, level, rating, duration."""

    min_rating = django_filters.NumberFilter(field_name="average_rating", lookup_expr="gte")
    max_price_cents = django_filters.NumberFilter(field_name="price_cents", lookup_expr="lte")
    min_duration = django_filters.NumberFilter(field_name="duration_minutes", lookup_expr="gte")
    max_duration = django_filters.NumberFilter(field_name="duration_minutes", lookup_expr="lte")

    class Meta:
        model = Course
        fields = {
            "pricing": ["exact"],
            "level": ["exact"],
            "category": ["exact"],
            "tags": ["exact"],
        }
