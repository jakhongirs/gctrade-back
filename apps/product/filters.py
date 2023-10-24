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

    def filter_manufacturer(self, queryset, name, value):
        manufacturers = value.split(",")
        return queryset.filter(manufacturer__id__in=manufacturers)

    def filter_category(self, queryset, name, value):
        categories = value.split(",")
        return queryset.filter(category__id__in=categories)

    class Meta:
        model = Product
        fields: list[str] = []
