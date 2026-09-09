from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("api/products", views.products),
    path("api/products/<int:id_>", views.products),
    path("api/carts", views.carts),
    path("api/carts/<int:id_>", views.carts)
]