from django.urls import path

from .views import FeedbackListView, PartnerListView

app_name = "partners"

urlpatterns = [
    path("", PartnerListView.as_view(), name="partners_list"),
    path("feedback/", FeedbackListView.as_view(), name="feedback_list"),
]
