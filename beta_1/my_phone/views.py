from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, Category

# Create your views here.
def home(request):
    user_list = ["Alex", "Mark", "Ivan"]
    isAdmin = True
    products = Product.objects.exclude(price__range=[20000, 35000]).exclude(
        category__name="Планшеты"
    )
    context = {
        "users": user_list,
        "isAdmin": isAdmin,
        "products": products
        }
    return render(request, "home.html", context)

def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        product = None
    context = {
        "product": product
    }
    return render(request, "product_detail.html", context)

def hello(request, name):
    name = name.upper()
    context = {
        "name": name
    }
    return render(request, "hello.html", context)

def helloid(request, id):
    return HttpResponse(f"Hello {id}!!!")
