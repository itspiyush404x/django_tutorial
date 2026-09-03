from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.shortcuts import render
import json
import os

# Create your views here.
def home(request):
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


    
