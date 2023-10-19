import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    manufacturer = django_filters.CharFilter(method="filter_manufacturer")
    category = django_filters.CharFilter(method="filter_category")
    is_recommended = django_filters.BooleanFilter(field_name="is_recommended")
    is_sale = django_filters.BooleanFilter(field_name="is_sale")
    is_active = django_filters.BooleanFilter(field_name="is_active")
    is_most_viewed = django_filters.BooleanFilter(field_name="views_count", method="filter_most_viewed")

    def filter_manufacturer(self, queryset, name, value):
        manufacturers = value.split(",")
        return queryset.filter(manufacturer__id__in=manufacturers)

    def filter_category(self, queryset, name, value):
        categories = value.split(",")
        return queryset.filter(category__id__in=categories)

    def filter_most_viewed(self, queryset, name, value):
        if value:
            return queryset.order_by("-views_count")
        return queryset

    class Meta:
        model = Product
        fields = []
