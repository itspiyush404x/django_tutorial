from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib import messages
import json
import os

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return HttpResponse(f"<h1>This is Home Page<h1/>")
    else:
        return redirect("login")
        

    if request.method == "GET":
        json_path = os.path.join(settings.MEDIA_ROOT, "data", "products.json")
        try:
            with open(json_path,"r") as file:
                raw_product = json.load(file)
        except json.JSONDecodeError:
            raw_product = {}

        products = []

        for product in raw_product:
            filename = product["img_filename"]
            img_url = f"{settings.MEDIA_URL}product_images/{filename}"

            product["img_url"] = img_url

            products.append(product)
        
        # return JsonResponse(products, safe=False)
        return render(request, "home.html", {"products":products})
    else:
        HttpResponse("Method not allowed", status=405)


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
    
