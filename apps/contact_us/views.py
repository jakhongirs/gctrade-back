from rest_framework import generics

from .models import ContactUs, EmployeeContact
from .serializers import ContactUsSerializer, EmployeeContactSerializer


class ContactUsRetrieveView(generics.RetrieveAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer

    def get_object(self):
        return ContactUs.objects.first()


class EmployeeContactListView(generics.ListAPIView):
    queryset = EmployeeContact.objects.all()
    serializer_class = EmployeeContactSerializer
