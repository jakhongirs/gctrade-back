from rest_framework import generics

from .models import AboutUs, ContactForm, ContactUs, EmployeeContact
from .serializers import (
    AboutUsSerializer, ContactFormSerializer, ContactUsSerializer,
    EmployeeContactSerializer
)


class ContactUsRetrieveView(generics.RetrieveAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer

    def get_object(self):
        return ContactUs.objects.first()


class EmployeeContactListView(generics.ListAPIView):
    queryset = EmployeeContact.objects.all()
    serializer_class = EmployeeContactSerializer


class ContactFormCreateView(generics.CreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer


class AboutUsRetrieveView(generics.RetrieveAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

    def get_object(self):
        return AboutUs.objects.first()
