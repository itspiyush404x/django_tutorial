from django.contrib import admin
from .models import Product, Cart, Category, Brand, ProductImage, VariantAttributeValue, Attribute, AttributeValue, ProductVariant

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(VariantAttributeValue)
admin.site.register(Attribute)
admin.site.register(AttributeValue)