from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from .filters import ProductFilter
from .models import (Banner, LastSeenProduct, Manufacturer, ParentCategory,
                     Product, ProductView)
from .serializers import (BannerSerializer, LastSeenProductSerializer,
                          ManufacturerSerializer, ParentCategorySerializer,
                          ProductSerializer)


class BannerListView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def get_queryset(self):
        return Banner.objects.filter(is_active=True).order_by("order")


class ManufacturerListView(generics.ListAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class ParentCategoryListView(generics.ListAPIView):
    queryset = ParentCategory.objects.all()
    serializer_class = ParentCategorySerializer


class ProductListView(generics.ListAPIView):
    """
    Multiple manufacturer, category can be filtered by comma separated values like: manufacturer=1,2,3 or category=1,2,3
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ("price", "views_count", "created_at", "-price", "-views_count", "-created_at")
    search_fields = ("title", "manufacturer__title", "category__title")

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by("-created_at")


class ProductDetailView(generics.RetrieveAPIView):
    """
    Fingerprint is required in headers
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_filtered_queryset(self):
        fingerprint = self.request.META.get("HTTP_FINGERPRINT", None)

        if fingerprint:
            ProductView.objects.get_or_create(product=self.get_object(), fingerprint=fingerprint)
            LastSeenProduct.objects.get_or_create(product=self.get_object(), fingerprint=fingerprint)

        return Product.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        self.queryset = self.get_filtered_queryset()
        return super().get(request, *args, **kwargs)


class LastSeenProductListView(generics.ListAPIView):
    """
    Fingerprint is required in headers
    """

    queryset = LastSeenProduct.objects.all()
    serializer_class = LastSeenProductSerializer

    def get_queryset(self):
        fingerprint = self.request.META.get("HTTP_FINGERPRINT", None)
        if fingerprint:
            return LastSeenProduct.objects.filter(fingerprint=fingerprint).order_by("-created_at")
        return LastSeenProduct.objects.none()
