from django.urls import path

from .views import (BannerListView, ManufacturerListView,
                    ParentCategoryListView, ProductListView)

app_name = "product"

urlpatterns = [
    path("banner/", BannerListView.as_view(), name="banner-list"),
    path("manufacturer/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("categories/", ParentCategoryListView.as_view(), name="categories-list"),
    path("products/", ProductListView.as_view(), name="products-list"),
]
