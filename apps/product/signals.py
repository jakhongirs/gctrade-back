from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.bot.utils import bot_send_message
from apps.product.choices import OrderStatusChoices
from apps.product.models import Order, ProductView


@receiver(post_save, sender=ProductView)
def update_product_views_count(sender, instance, created, **kwargs):
    if created:
        count = ProductView.objects.filter(product=instance.product).count()

        instance.product.views_count = count
        instance.product.save()


@receiver(post_delete, sender=ProductView)
def update_product_views_count_after_delete(sender, instance, **kwargs):
    count = ProductView.objects.filter(product=instance.product).count()

    instance.product.views_count = count
    instance.product.save()


@receiver(post_save, sender=Order)
def send_order_message(sender, instance, created, **kwargs):
    if created:
        bot_send_message("IN MODERATION")
    if instance.status == OrderStatusChoices.SOLD:
        bot_send_message("SOLD")
    if instance.status == OrderStatusChoices.CANCELED:
        bot_send_message("CANCELED")
