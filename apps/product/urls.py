from django.urls import path

from apps.product.views import (
    BannerListView, CartCreateView, CartItemCreateView, CartItemDeleteView,
    CartItemsListView, CartItemUpdateView, CartListView,
    LastSeenProductListView, ManufacturerByCategoryListView,
    ManufacturerListView, ParentCategoryListView, ProductDetailView,
    ProductListView, SavedProductCreateView, SavedProductListView
)

app_name = "product"

urlpatterns = [
    path("list/", ProductListView.as_view(), name="products-list"),
    path("detail/<slug:slug>/", ProductDetailView.as_view(), name="products-detail"),
    path("banner/", BannerListView.as_view(), name="banner-list"),
    path("manufacturer/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("categories/", ParentCategoryListView.as_view(), name="categories-list"),
    path("last-seen-products/", LastSeenProductListView.as_view(), name="last-seen-products-list"),
    path("manufacturer/<int:category_id>/", ManufacturerByCategoryListView.as_view(), name="manufacturer-by-category"),
    path("saved-products/", SavedProductListView.as_view(), name="saved-products-list"),
    path("saved-products/create/", SavedProductCreateView.as_view(), name="saved-products-create"),
    # Cart
    path("cart/create/", CartCreateView.as_view(), name="cart-create"),
    path("cart/list/", CartListView.as_view(), name="cart-detail"),
    path("cart-item/create/", CartItemCreateView.as_view(), name="cart-item-create"),
    path("cart-item/update/<int:pk>/", CartItemUpdateView.as_view(), name="cart-item-update"),
    path("cart-item/delete/<int:pk>/", CartItemDeleteView.as_view(), name="cart-item-delete"),
    path("cart-items/<int:cart_id>/", CartItemsListView.as_view(), name="cart-items-list"),
]
