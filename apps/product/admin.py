from django.contrib import admin
from django.contrib.admin.options import TabularInline

from .models import (Banner, Category, Manufacturer, ParentCategory, Product,
                     ProductGallery)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("title", "sub_title")


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(ParentCategory)
class ParentCategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "parent",
    )
    list_filter = ("parent",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("parent",)


class ProductGalleryInline(TabularInline):
    model = ProductGallery
    extra = 0
    autocomplete_fields = ("product",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "in_stock_count")
    list_filter = ("category", "manufacturer", "is_active", "is_recommended", "is_sale")
    search_fields = ("title", "manufacturer__title", "category__title")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("category", "manufacturer")
    readonly_fields = ("views_count",)
    inlines = (ProductGalleryInline,)
