from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.product.filters import ProductFilter
from apps.product.models import (
    Banner, Cart, CartItem, LastSeenProduct, Manufacturer, Order,
    ParentCategory, Product, ProductView, SavedProduct, SearchHistory
)
from apps.product.serializers import (
    BannerSerializer, CartItemCreateSerializer, CartItemListSerializer,
    CartSerializer, LastSeenProductSerializer, ManufacturerSerializer,
    OrderSerializer, ParentCategorySerializer, ProductSerializer,
    SavedProductCreateSerializer, SavedProductSerializer,
    SearchHistorySerializer
)


@method_decorator(cache_page(60 * 20), name="dispatch")
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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("id", "categories__id", "slug", "categories__slug")


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
        return (
            Product.objects.filter(is_active=True)
            .order_by("-created_at")
            .select_related("manufacturer", "category")
            .prefetch_related("gallery")
        )


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


class ManufacturerByCategoryListView(generics.ListAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    lookup_field = "category_id"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Manufacturer.objects.filter(product__category_id=category_id).distinct()


class SavedProductListView(generics.ListAPIView):
    """
    Fingerprint is required in headers
    """

    queryset = SavedProduct.objects.all()
    serializer_class = SavedProductSerializer

    def get_queryset(self):
        fingerprint = self.request.META.get("HTTP_FINGERPRINT", None)
        if fingerprint:
            return SavedProduct.objects.filter(fingerprint=fingerprint).order_by("-created_at")
        return SavedProduct.objects.none()


class SavedProductCreateView(generics.CreateAPIView):
    queryset = SavedProduct.objects.all()
    serializer_class = SavedProductCreateSerializer


class SavedProductDeleteView(generics.DestroyAPIView):
    queryset = SavedProduct.objects.all()
    serializer_class = SavedProductCreateSerializer


class CartCreateView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartListView(generics.ListAPIView):
    """
    Fingerprint is required in headers
    """

    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        fingerprint = self.request.META.get("HTTP_FINGERPRINT", None)
        if fingerprint:
            return Cart.objects.filter(fingerprint=fingerprint).order_by("-created_at")
        return Cart.objects.none()


class CartItemCreateView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer


class CartItemUpdateView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer


class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer


class CartItemsListView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer
    lookup_field = "cart_id"

    def get_queryset(self):
        cart_id = self.kwargs.get("cart_id")
        return CartItem.objects.filter(cart_id=cart_id).order_by("-created_at")


class CartTotalPriceView(APIView):
    """
    Fingerprint is required in headers
    """

    def get(self, request, *args, **kwargs):
        fingerprint = self.request.META.get("HTTP_FINGERPRINT", None)
        cart_id = self.kwargs.get("cart_id")

        if fingerprint:
            cart = Cart.objects.filter(fingerprint=fingerprint, pk=cart_id).first()

            if cart:
                total_quantity = cart.items.count()
                total_price = cart.total_price

                # Calculate total savings from sales
                total_savings = 0
                for cart_item in cart.items.all():
                    product = cart_item.product
                    if product.sale_price is not None:
                        savings_per_item = (product.price - product.sale_price) * cart_item.quantity
                        total_savings += savings_per_item

                return Response(
                    {
                        "quantity": total_quantity,
                        "total_price": total_price,
                        "total_savings": total_savings,
                    }
                )

        return Response({"total_price": 0, "total_savings": 0, "quantity": 0})


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class SearchHistoryCreateView(generics.CreateAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer


class SearchHistoryListView(generics.ListAPIView):
    """
    Fingerprint is required in headers
    """

    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer

    def get_queryset(self):
        fingerprint = self.request.META.get("HTTP_FINGERPRINT", None)
        if fingerprint:
            return SearchHistory.objects.filter(fingerprint=fingerprint).order_by("-created_at")[0:5]
        return SearchHistory.objects.none()


class SearchHistoryDeleteView(generics.DestroyAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    lookup_field = "pk"

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        fingerprint = self.request.META.get("HTTP_FINGERPRINT", None)

        if fingerprint:
            search_history = SearchHistory.objects.filter(fingerprint=fingerprint, pk=pk).first()
            if search_history:
                search_history.delete()
                return Response({"status": "deleted"})
            return Response({"status": "not found"})
        return Response({"status": "please provide fingerprint"})


class PopularSearchHistoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            popular_searches = (
                SearchHistory.objects.values("query").annotate(count=Count("query")).order_by("-count")[:5]
            )
            popular_searches_list = list(popular_searches.values("query", "count"))
            return Response({"popular_searches": popular_searches_list})
        except Exception as e:
            return Response({"error": str(e)})
