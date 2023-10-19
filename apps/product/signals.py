from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.product.models import ProductView


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
