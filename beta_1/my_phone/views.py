from django.shortcuts import render
from django.http import HttpResponse

from .models import Product

# Create your views here.
def home(request):
    user_list = ["Alex", "Mark", "Ivan"]
    isAdmin = True
    products = Product.objects.filter(price__lte=25000)
    context = {
        "users": user_list,
        "isAdmin": isAdmin,
        "products": products
        }
    return render(request, "home.html", context)

def hello(request, name):
    name = name.upper()
    context = {
        "name": name
    }
    return render(request, "hello.html", context)

def helloid(request, id):
    return HttpResponse(f"Hello {id}!!!")
