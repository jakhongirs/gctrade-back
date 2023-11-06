from django.urls import path

from apps.product.views import (
    BannerListView, CartCreateView, CartItemCreateView, CartItemDeleteView,
    CartItemsListView, CartItemUpdateView, CartListView, CartTotalPriceView,
    LastSeenProductListView, ManufacturerListView, OrderCreateView,
    ParentCategoryListView, PopularSearchHistoryAPIView, ProductDetailView,
    ProductListView, SavedProductCreateView, SavedProductDeleteView,
    SavedProductListView, SearchHistoryCreateView, SearchHistoryDeleteView,
    SearchHistoryListView
)

app_name = "product"

urlpatterns = [
    # Product
    path("list/", ProductListView.as_view(), name="products-list"),
    path("detail/<slug:slug>/", ProductDetailView.as_view(), name="products-detail"),
    path("banner/", BannerListView.as_view(), name="banner-list"),
    path("manufacturer/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("categories/", ParentCategoryListView.as_view(), name="categories-list"),
    path("last-seen-products/", LastSeenProductListView.as_view(), name="last-seen-products-list"),
    path("saved-products/", SavedProductListView.as_view(), name="saved-products-list"),
    path("saved-products/create/", SavedProductCreateView.as_view(), name="saved-products-create"),
    path("saved-products/delete/<int:pk>/", SavedProductDeleteView.as_view(), name="saved-products-delete"),
    path("search-history/", SearchHistoryListView.as_view(), name="search-history-list"),
    path("search-history/create/", SearchHistoryCreateView.as_view(), name="search-history-create"),
    path("search-history/delete/<int:pk>/", SearchHistoryDeleteView.as_view(), name="search-history-delete"),
    path("popular-search-history/", PopularSearchHistoryAPIView.as_view(), name="popular-search-history-list"),
    # Cart & Order
    path("cart/create/", CartCreateView.as_view(), name="cart-create"),
    path("cart/list/", CartListView.as_view(), name="cart-detail"),
    path("cart-item/create/", CartItemCreateView.as_view(), name="cart-item-create"),
    path("cart-item/update/<int:pk>/", CartItemUpdateView.as_view(), name="cart-item-update"),
    path("cart-item/delete/<int:pk>/", CartItemDeleteView.as_view(), name="cart-item-delete"),
    path("cart-items/<int:cart_id>/", CartItemsListView.as_view(), name="cart-items-list"),
    path("cart/total-price/<int:cart_id>/", CartTotalPriceView.as_view(), name="cart-total-price"),
    path("order/create/", OrderCreateView.as_view(), name="order-create"),
]
