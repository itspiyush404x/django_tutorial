from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.contrib.auth.models import User, auth
from main.models import Product, Cart
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json
import os

from main.Utils.validation import valid_product, valid_cart




# Create your views here.
def home(request):
    
    return render(request, "home.html", )


    # if request.method == "GET":
    #     json_path = os.path.join(settings.MEDIA_ROOT, "data", "products.json")
    #     try:
    #         with open(json_path,"r") as file:
    #             raw_product = json.load(file)
    #     except json.JSONDecodeError:
    #         raw_product = {}

    #     products = []

    #     for product in raw_product:
    #         filename = product["img_filename"]
    #         img_url = f"{settings.MEDIA_URL}product_images/{filename}"

    #         product["img_url"] = img_url

    #         products.append(product)
        
    #     # return JsonResponse(products, safe=False)
    #     return render(request, "home.html", {"products":products})
    # else:
    #     HttpResponse("Method not allowed", status=405)


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



#----------- e-commarce --------------------------

@csrf_exempt
def products(request, id_=None):
    if id_ is None:
        if request.method == "GET":
            return get_all_products(request)
        elif request.method == "POST":
            return post_product(request)
        else:
            return HttpResponse(status=405)
    else:
        if request.method == "GET":
            return get_single_product(request, id_)
        elif request.method == "PUT":
            return update_product(request, id_)
        elif request.method == "DELETE":
            return delete_product(request, id_)
        else:
            return HttpResponse(status=405)


def post_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
       
        title = data.get("title", "")
        price = data.get("price", 0)
        description = data.get("description", "")
        category = data.get("category", "")
        image = data.get("image", "")

        valid = valid_product({"title": title, "price": price, "description": description, "category": category, "image": image})
        if  valid is True:
            try:
                product = Product.objects.create(title=title, price=price, description=description, category=category, image=image)
                product.save()
            except IntegrityError:
                return JsonResponse({"error":["product of same title already exits"]}, status=400)
            return HttpResponse(status=201)
        else:
            return HttpResponse(valid["error"], status=400)
    else:
        return HttpResponse(status=405)

def get_all_products(request):
    products = list(Product.objects.values())
    return JsonResponse(products, safe=False, status=200)

def get_single_product(request, id_):
    try:
        product = Product.objects.values().get(id=id_)
        return JsonResponse(product, safe=False, status=200)
    except Product.DoesNotExist:
        return JsonResponse({"error":"Product Does not exist"}, status=404)

def update_product(request, id_):
    try:
        product = Product.objects.get(id=id_)

        data = json.loads(request.body)
        try:
            title = data.get("title")
            price = data.get("price")
            description = data.get("description")
            category = data.get("category")
            image = data.get("image")
        except KeyError:
            return JsonResponse({"error":"Invalid json"}, status=422)

        product.title = title
        product.price = price
        product.description = description
        product.category = category
        product.image = image
        
        product.save()

        return HttpResponse(status=200)
    except Product.DoesNotExist:
        return JsonResponse({"error":"Product Does not exist"}, status=404)

def delete_product(request, id_):
    try:
        product = Product.objects.get(id=id_)
        product.delete()
        return HttpResponse(status=204)
    except Product.DoesNotExist:
        return JsonResponse({"error":"Product Does not exist"}, status=404)





@csrf_exempt
def carts(request, id_=None):
    if id_ is None:
        if request.method == "GET":
            return get_all_cart(request)
        elif request.method == "POST":
            return post_cart(request)
        else:
            return HttpResponse(status=405)
    else:
        if request.method == "GET":
            return get_single_cart(request, id_)
        elif request.method == "PUT":
            return update_cart(request, id_)
        elif request.method == "DELETE":
            return delete_cart(request, id_)
        else:
            return HttpResponse(status=405)


def post_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username", "")
        products = data.get("products", [])

        valid = valid_cart({"username":username, "products":products})
        if valid is not True:
            return HttpResponse(valid["error"], status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error":"User not exits"},status=404)

        cart = Cart.objects.create(user=user)
        cart.save()

        if products:
            for prod in products:
                product = Product.objects.get(id=prod["id"])
                cart.products.add(product)
        
        cart.save()

        return HttpResponse(status=201)

def get_all_cart(request):
    data = Cart.objects.all()

    carts = []
    for cart in data:
        carts.append({"id":cart.id, "username":cart.user.username, "products":[list(cart.products.values())]})
    
    return JsonResponse(carts, safe=False, status=200)

def get_single_cart(request, id_):
    try:
        cart = Cart.objects.get(id=id_)
    except Cart.DoesNotExist:
        return JsonResponse({"error":"Cart does not exit"},status=404)

    cart_dict = {"id":cart.id, "username":cart.user.username, "products":[list(cart.products.values())]}
    return JsonResponse(cart_dict, status=200)

def update_cart(request, id_):
    try:
        cart = Cart.objects.get(id=id_)
    except Cart.DoesNotExist:
        return JsonResponse({"error":"Cart does not exit"},status=404)

    data = json.loads(request.body)
    try:
        username = data.get("username")
        products = data.get("products")
    except KeyError:
        return JsonResponse({"error":"Invalid json"}, status=422)

    try:
        user = User.objects.get(username=username)
        cart.user = user
    except User.DoesNotExist:
        return JsonResponse({"error":"User does not exit"},status=404)


    new_produts = []
    for prod in products:
        try:
            product = Product.objects.get(id=prod["id"])
            new_produts.append(product)
        except Product.DoesNotExist:
            return JsonResponse({"error":f"Product with id={prod_id} does not exit"},status=404)
    
    cart.products.clear()
    cart.products.add(*new_produts)

    return HttpResponse(status=200)

def delete_cart(request, id_):
    try:
        cart = Cart.objects.get(id=id_)
    except Cart.DoesNotExist:
        return JsonResponse({"error":"Cart does not exit"},status=404)

    cart.delete()
    return HttpResponse(status=204)


