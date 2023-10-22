from rest_framework import generics

from .models import ContactForm, ContactUs, EmployeeContact
from .serializers import (ContactFormSerializer, ContactUsSerializer,
                          EmployeeContactSerializer)


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
