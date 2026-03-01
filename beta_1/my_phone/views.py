from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum, Avg, Min, Max , F

from .models import Product, Category
from .forms import CategoryForm, ProductForm

# Create your views here.
def home(request):
    user_list = ["Alex", "Mark", "Ivan"]
    isAdmin = True
    products = Product.objects.filter(price__lte=25000).order_by("-price", "name")
    # category = Category.objects.get(name="ТЕЛЕФОНЫ")
    # products = category.product.all()
    summ = Product.objects.aggregate(Avg("price"))
    print(summ)
    context = {
        "users": user_list,
        "isAdmin": isAdmin,
        "products": products
        }
    return render(request, "home.html", context)

def product_detail(request, id):
    try:
        product = Product.objects.filter(id=id).update(price=F('price') + 1)
    except Product.DoesNotExist:
        product = None
    # if product:
    #     product.price += 1
    #     product.save()
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


def form_view(request):
    if request.method == "GET":
        form = CategoryForm()
        context = {
            "form" : form
        }
        return render(request, "form.html", context=context)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            form = CategoryForm()
            return redirect("home")
            # return render(request, "form.html", context={"form" : form})
        context = {"form": form}
        return render(request, "form.html", context=context)


def product_form_view(request):
    if request.method == "GET":
        form = ProductForm()
        context = {"form": form}
        return render(request, "create_product.html", context=context)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = ProductForm()
            return redirect("home")
        context = {"form": form}
        return render(request, "create_product.html", context=context)
