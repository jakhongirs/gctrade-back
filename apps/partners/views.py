from rest_framework import generics

from .models import Partner
from .serializers import PartnerSerializer


class PartnerListView(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

    def get_queryset(self):
        return Partner.objects.order_by("order")
