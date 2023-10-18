from rest_framework import serializers

from apps.common.serializers import ImageSerializer

from .models import Banner, Category, Manufacturer, ParentCategory, Product


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ("id", "title", "sub_title", "image", "is_active", "url", "product", "order")


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ("id", "title", "logo")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "slug", "parent")


class ParentCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = ParentCategory
        fields = ("id", "title", "slug", "icon", "categories")


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    gallery = ImageSerializer(many=True, source="get_gallery")

    class Meta:
        model = Product
        fields = (
            "id",
            "manufacturer",
            "category",
            "title",
            "slug",
            "description",
            "features",
            "price",
            "in_stock_count",
            "views_count",
            "is_recommended",
            "is_active",
            "is_sale",
            "gallery",
        )
