from django.db import models
from django.contrib.auth.models import User
from .Utils.helper import product_image_path_name, brand_logo_path_name
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=3000)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=3000)
    logo = models.ImageField(upload_to=brand_logo_path_name)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=3000)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)

    base_price = models.DecimalField(max_digits=30, decimal_places=2)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="variats")

    name = models.CharField(max_length=250, unique=True, blank=True)

    price = models.DecimalField(max_digits=30, decimal_places=2)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def build_name(self):
        values = (
            self.attributes
            .select_related("attribute", "attribute_value")
            .order_by("attribute__name")
            .values_list("attribute_value__value", flat=True)
        )

        return f"{self.product.name} - {"/ ".join(values)}"

    def __str__(self):
        return self.name

    def update_name(self):
        self.name = self.build_name()
        ProductVariant.objects.filter(pk=self.pk).update(name=self.name)
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.product.name
        super().save(*args, **kwargs)


class Attribute(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="values"
        )

    value = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class VariantAttributeValue(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="attributes"
        )

    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="+",        # no reverse accessor needed
        editable=False,         # set automatically, not by hand
    )
    
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="variant_attributes"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["variant", "attribute"],
                name="unique_variant_attribute",
            )
        ]

    def __str__(self):
        return f"{self.variant.name} → {self.attribute.name}: {self.attribute_value.value}"
    
    
    def save(self, *args, **kwargs):
        self.attribute_id = self.attribute_value.attribute_id

        super().save(*args, **kwargs)

        self.variant.update_name()

    def delete(self, *args, **kwargs):
        variant = self.variant

        super().delete(*args, **kwargs)

        variant.update_name()


# Backward-compatible alias for older code/tests that still refer to the
# historical VariantAttribute name.
VariantAttribute = VariantAttributeValue
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="images")
    variant = models.ManyToManyField(ProductVariant, null=True, related_name="images")
    url = models.ImageField(upload_to=product_image_path_name)

    display_order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.product.slug}-image"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)


