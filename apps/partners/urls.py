from django.urls import path

from .views import PartnerListView

app_name = "partners"

urlpatterns = [
    path("", PartnerListView.as_view(), name="partners_list"),
]
