from django.urls import path

from .views import (BannerListView, LastSeenProductListView,
                    ManufacturerByCategoryListView, ManufacturerListView,
                    ParentCategoryListView, ProductDetailView, ProductListView)

app_name = "product"

urlpatterns = [
    path("list/", ProductListView.as_view(), name="products-list"),
    path("detail/<slug:slug>/", ProductDetailView.as_view(), name="products-detail"),
    path("banner/", BannerListView.as_view(), name="banner-list"),
    path("manufacturer/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("categories/", ParentCategoryListView.as_view(), name="categories-list"),
    path("last-seen-products/", LastSeenProductListView.as_view(), name="last-seen-products-list"),
    path("manufacturer/<int:category_id>/", ManufacturerByCategoryListView.as_view(), name="manufacturer-by-category"),
]
