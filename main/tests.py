from django.test import TestCase
from django.urls import reverse

from API.models import (
    Attribute,
    AttributeValue,
    Product,
    ProductVariant,
    VariantAttributeValue,
)


class ProductDetailAttributeTests(TestCase):
    def test_all_attributes_are_shown_and_single_option_is_selected(self):
        product = Product.objects.create(
            name="Cotton T-shirt",
            description="A cotton T-shirt.",
            base_price="20.00",
        )
        color = Attribute.objects.create(name="Color")
        size = Attribute.objects.create(name="Size")
        fabric = Attribute.objects.create(name="Fabric")

        variants = []
        for color_value, size_value in (
            ("Black", "S"),
            ("Black", "M"),
            ("White", "S"),
            ("White", "M"),
        ):
            variant = ProductVariant.objects.create(
                product=product,
                name=f"Cotton T-shirt {color_value} {size_value}",
                price="20.00",
            )
            variants.append((variant, color_value, size_value))

        for variant, color_value, size_value in variants:
            for attribute, value in (
                (color, color_value),
                (size, size_value),
                (fabric, "Cotton"),
            ):
                attribute_value, _ = AttributeValue.objects.get_or_create(
                    attribute=attribute,
                    value=value,
                )
                VariantAttributeValue.objects.create(
                    variant=variant,
                    attribute_value=attribute_value,
                )

        response = self.client.get(reverse("product_detail", args=[product.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-attribute="Color"')
        self.assertContains(response, 'data-attribute="Size"')
        self.assertContains(response, 'data-attribute="Fabric" disabled')
        self.assertContains(response, '<option value="Cotton" selected>')
