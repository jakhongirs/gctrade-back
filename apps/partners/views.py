from rest_framework import generics

from .models import Feedback, Partner
from .serializers import FeedbackSerializer, PartnerSerializer


class PartnerListView(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

    def get_queryset(self):
        return Partner.objects.order_by("order")


class FeedbackListView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return Feedback.objects.order_by("created_at")
