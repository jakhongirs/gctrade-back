from decimal import Decimal

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.common.utils import generate_unique_slug


class Manufacturer(BaseModel):
    title = models.CharField(max_length=250, verbose_name=_("Title"))
    logo = models.ImageField(upload_to="manufacturer", verbose_name=_("Logo"), blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Manufacturer")
        verbose_name_plural = _("Manufacturers")


class ParentCategory(BaseModel):
    title = models.CharField(max_length=250, verbose_name=_("Title"))
    slug = models.SlugField(max_length=250, verbose_name=_("Slug"), unique=True)
    icon = models.ImageField(upload_to="category", verbose_name=_("Icon"), blank=True, null=True)

    def clean(self):
        if not self.icon:
            raise ValidationError({"icon": _("Icon is required for parent category")})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.title)
        super(ParentCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Parent Category")
        verbose_name_plural = _("Parent Categories")


class Category(BaseModel):
    title = models.CharField(max_length=250, verbose_name=_("Title"))
    slug = models.SlugField(max_length=250, verbose_name=_("Slug"), unique=True)
    parent = models.ForeignKey(
        "product.ParentCategory", on_delete=models.CASCADE, verbose_name=_("Parent"), related_name="categories"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Product(BaseModel):
    manufacturer = models.ForeignKey(
        "product.Manufacturer", on_delete=models.CASCADE, verbose_name=_("Manufacturer"), blank=True, null=True
    )
    category = models.ForeignKey("product.Category", on_delete=models.CASCADE, verbose_name=_("Category"))
    title = models.CharField(max_length=250, verbose_name=_("Title"))
    slug = models.SlugField(max_length=250, verbose_name=_("Slug"), unique=True)
    description = RichTextUploadingField(verbose_name=_("Description"), blank=True, null=True)
    features = RichTextUploadingField(verbose_name=_("Features"), blank=True, null=True)
    price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_("Price"), default=Decimal("0"))
    in_stock_count = models.PositiveIntegerField(verbose_name=_("In Stock Count"), default=0)
    views_count = models.PositiveIntegerField(verbose_name=_("Views Count"), default=0)
    is_recommended = models.BooleanField(default=False, verbose_name=_("Is Recommended"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    is_sale = models.BooleanField(default=False, verbose_name=_("Is Sale"))

    def get_gallery(self):
        return self.gallery.all()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductGallery(models.Model):
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, verbose_name=_("Product"), related_name="gallery"
    )
    image = models.ImageField(upload_to="product/gallery", verbose_name=_("Image"))

    def __str__(self):
        return self.product.title


class Banner(BaseModel):
    title = models.CharField(max_length=250, verbose_name=_("Title"), blank=True, null=True)
    sub_title = models.CharField(max_length=250, verbose_name=_("Sub Title"), blank=True, null=True)
    image = models.ImageField(upload_to="banner", verbose_name=_("Image"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    url = models.URLField(verbose_name=_("URL"), blank=True, null=True)
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, verbose_name=_("Product"), blank=True, null=True
    )
    order = models.PositiveIntegerField(verbose_name=_("Order"), default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")
