from django.urls import path

from .views import BannerListView

app_name = "product"

urlpatterns = [
    path("banner/", BannerListView.as_view(), name="banner-list"),
]
