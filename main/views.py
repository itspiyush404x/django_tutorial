# Standard Library Imports
import json
import os

# Third-Party Library Imports (Django)
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Prefetch
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

# Third-Party Library Imports (Django REST Framework)
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

# Local Application / Custom Imports
from decorators import rate_limit_fixed_window, rate_limit_sliding_window
from API.models import Product, ProductImage, VariantAttributeValue, Cart






# Create your views here.
def home(request):
    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)

    products = (
        Product.objects.filter(is_active=True)
        .select_related("brand", "category")
        .prefetch_related(
            Prefetch(
                "images",
                queryset=ProductImage.objects.order_by(
                    "-is_primary", "display_order", "id"
                ),
            )
        )
    )
    return render(request, "home1.html", {"products": products})


def product_detail(request, slug):
    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)

    product = get_object_or_404(
        Product.objects.filter(is_active=True)
        .select_related("brand", "category")
        .prefetch_related(
            Prefetch(
                "images",
                queryset=ProductImage.objects.order_by(
                    "-is_primary", "display_order", "id"
                ),
            ),
        ),
        slug=slug,
    )
    variants = (
        product.variats.filter(is_active=True)
        .prefetch_related(
            Prefetch(
                "attributes",
                queryset=VariantAttributeValue.objects.select_related(
                    "attribute_value__attribute"
                ).order_by("id"),
            ),
            Prefetch(
                "images",
                queryset=ProductImage.objects.order_by(
                    "-is_primary", "display_order", "id"
                ),
            ),
        )
        .order_by("id")
    )

    option_groups = {}
    variants_data = []
    for variant in variants:
        attributes = {}
        display_attributes = []
        for variant_attribute in variant.attributes.all():
            attribute = variant_attribute.attribute_value.attribute
            value = variant_attribute.attribute_value.value
            attributes[attribute.name] = value
            normalized_name = attribute.name.strip().casefold()
            if normalized_name in {"color", "colour"}:
                label = "Colour"
            elif normalized_name in {
                "storage",
                "memory",
                "storage capacity",
                "memory storage capacity",
            }:
                label = "Storage"
            else:
                label = attribute.name
            display_attributes.append({"label": label, "value": value})
            group = option_groups.setdefault(
                attribute.name,
                {"name": attribute.name, "label": label, "values": []},
            )
            if value not in group["values"]:
                group["values"].append(value)

        variants_data.append(
            {
                "id": variant.id,
                "name": variant.name,
                "price": str(variant.price),
                "is_active": variant.is_active,
                "attributes": attributes,
                "display_attributes": display_attributes,
                "images": [
                    {"url": image.url.url, "alt": product.name}
                    for image in variant.images.all()
                ],
            }
        )

    option_groups = sorted(
        option_groups.values(),
        key=lambda group: (
            0
            if group["label"] == "Colour"
            else 1
            if group["label"] == "Storage"
            else 2,
            group["label"].casefold(),
        ),
    )
    default_attributes = variants_data[0]["attributes"] if variants_data else {}
    for group in option_groups:
        group["default_value"] = default_attributes.get(group["name"], "")

    product_images = [
        {"url": image.url.url, "alt": product.name}
        for image in product.images.all()
    ]
    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "option_groups": option_groups,
            "variants_data": variants_data,
            "default_variant": variants_data[0] if variants_data else None,
            "product_images": product_images,
        },
    )





def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password != password2:
            messages.info(request, "Passwords are not matching")
            return redirect("register")
        else: # password == password2
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already used")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exist")
                return redirect("register")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect("login")
    else:
        return render(request, "register.html")
    
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(username, password)

        user = auth.authenticate(username=username, password=password)

        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Incorrect Credentials")
            return redirect("login")
    else:
        return render(request, "login.html")
    
def logout(request):
    auth.logout(request)
    return redirect("home")
