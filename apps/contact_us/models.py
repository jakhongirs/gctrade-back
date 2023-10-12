from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Phone(BaseModel):
    phone = models.CharField(_("Phone"), max_length=255)

    class Meta:
        verbose_name = _("Phone")
        verbose_name_plural = _("Phones")

    def __str__(self):
        return self.phone


class SocialMedia(BaseModel):
    name = models.CharField(_("Name"), max_length=255)
    url = models.URLField(_("URL"), max_length=255)

    class Meta:
        verbose_name = _("Social Media")
        verbose_name_plural = _("Social Media")

    def __str__(self):
        return self.name


class ContactUs(BaseModel):
    phone = models.ManyToManyField(Phone, verbose_name=_("Phone"), blank=True)
    email = models.EmailField(_("Email"), max_length=255, null=True, blank=True)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True)
    latitude = models.FloatField(_("Latitude"), null=True, blank=True)
    address = models.CharField(_("Address"), max_length=255)
    social_media = models.ManyToManyField(SocialMedia, verbose_name=_("Social Media"), blank=True)

    class Meta:
        verbose_name = _("Contact Us")
        verbose_name_plural = _("Contact Us")

    def __str__(self):
        return self.address


class EmployeeContact(BaseModel):
    name = models.CharField(_("Name"), max_length=255)
    image = models.ImageField(_("Image"), upload_to="employee_contact", null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=255)
    email = models.EmailField(_("Email"), max_length=255, null=True, blank=True)
    telegram_username = models.CharField(_("Telegram Username"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Employee Contact")
        verbose_name_plural = _("Employee Contacts")

    def __str__(self):
        return self.name
