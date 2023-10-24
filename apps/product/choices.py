from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatusChoices(models.TextChoices):
    IN_MODERATION = "in_moderation", _("Moderatsiyada")
    SOLD = "sold", _("Sotildi")
    CANCELED = "canceled", _("Bekor qilindi")
