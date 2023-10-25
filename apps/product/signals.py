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
    message = f"""
🏷️ Status: <b>{instance.get_status_display()}</b>

🆔 Buyurtma ID: {instance.pk}
👤 Ism: {instance.name}
📞 Telefon: {instance.phone}
📅 Sana: {instance.created_at.strftime("%Y-%m-%d %H:%M")}
"""

    message += f"""
🧾 Jami: {instance.cart.total_price}
"""

    message += f"""
📎 <a href='https://gctrade.uz/admin/product/order/{instance.pk}/change/'>Admin Panel</a>
"""

    if created or (instance.status in [OrderStatusChoices.SOLD, OrderStatusChoices.CANCELED]):
        # Check if a message for the current status has been sent before
        if not Order.objects.filter(pk=instance.pk, status=instance.status, bot_message_sent=True).exists():
            bot_send_message(message)
            instance.bot_message_sent = True  # Mark the message as sent
            instance.save()


@receiver(post_save, sender=Order)
def update_product_quantity(sender, instance, created, **kwargs):
    if instance.status == OrderStatusChoices.SOLD:
        order_item = instance.cart.items.first()
        if order_item and order_item.product:
            count = Order.objects.filter(
                cart__items__product=order_item.product, status=OrderStatusChoices.SOLD
            ).count()

            order_item.product.in_stock_count -= count
            order_item.product.save()
