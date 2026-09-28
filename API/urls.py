from django.urls import path
from . import views

urlpatterns = [
    path("products", views.ProductListCreate.as_view()),
    path("products/<int:pk>", views.ProductDetail.as_view()),

    path("carts", views.carts),
    path("carts/<int:id_>", views.carts)
]