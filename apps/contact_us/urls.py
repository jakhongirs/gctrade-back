from django.urls import path

from .views import (ContactFormCreateView, ContactUsRetrieveView,
                    EmployeeContactListView)

app_name = "contact_us"

urlpatterns = [
    path("", ContactUsRetrieveView.as_view(), name="contact_us"),
    path("employee_contact/", EmployeeContactListView.as_view(), name="employee_contact"),
    path("contact_form/", ContactFormCreateView.as_view(), name="contact_form"),
]
