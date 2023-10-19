from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class Partner(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    logo = models.ImageField(upload_to="partners", verbose_name=_("Logo"))
    url = models.URLField(verbose_name=_("URL"), blank=True, null=True)
    order = models.PositiveIntegerField(verbose_name=_("Order"), default=0)

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")

    def __str__(self):
        return self.name


class Company(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    logo = models.ImageField(upload_to="companies", verbose_name=_("Logo"))
    url = models.URLField(verbose_name=_("URL"), blank=True, null=True)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name


class Feedback(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_("Company"))
    text = models.TextField(verbose_name=_("Text"))

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")

    def __str__(self):
        return self.company.name
