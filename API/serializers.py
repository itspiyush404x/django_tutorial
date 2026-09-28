from rest_framework import serializers
from .models import Product, Category, Brand, ProductImage


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "name")

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ("id", "name")

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ("id", "url")

# class ProductVariantSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProductVariant
#         fields = ()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(read_only=True, many=True)


    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "base_price",
            "images",
            "variats",
            "is_active",
            "created_at",
            "updated_at",
            "category",
            "brand",
        ]

