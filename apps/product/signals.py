from django.db.models.signals import post_delete, post_save, pre_save
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


@receiver(pre_save, sender=Order)
def send_order_message(sender, instance, **kwargs):
    message = f"""
🏷️ Статус: {instance.get_status_display()}

🆔 ID заказа: {instance.pk}
👤 Имя: {instance.name}
📞 Телефон: {instance.phone}
📅 Дата: {instance.created_at.strftime("%Y-%m-%d %H:%M")}
"""

    message += f"""
🧾 Итого: {instance.cart.total_price} сум
"""

    message += f"""
https://gctrade.uz/admin/product/order/{instance.pk}/change/
"""

    if instance.pk:
        old_instance = Order.objects.get(pk=instance.pk)

        if old_instance.status != instance.status:
            bot_send_message(message, instance.pk)


@receiver(post_save, sender=Order)
def update_product_quantity(sender, instance, created, **kwargs):
    if instance.status == OrderStatusChoices.SOLD and not instance.in_stock_subtracted:
        order_item = instance.cart.items.first()
        if order_item and order_item.product:
            order_item.product.in_stock_count -= 1
            order_item.product.save()

            instance.in_stock_subtracted = True
            instance.save()
    elif not created and instance.status != OrderStatusChoices.SOLD and instance.in_stock_subtracted:
        order_item = instance.cart.items.first()
        if order_item and order_item.product:
            order_item.product.in_stock_count += 1
            order_item.product.save()

            instance.in_stock_subtracted = False
            instance.save()
