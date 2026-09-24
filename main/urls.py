from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),

    path("api/products", views.ProductListCreate.as_view()),
    path("api/products/<int:pk>", views.ProductDetail.as_view()),

    path("api/carts", views.carts),
    path("api/carts/<int:id_>", views.carts)
]