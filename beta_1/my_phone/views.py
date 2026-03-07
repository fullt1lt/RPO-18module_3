from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum, Avg, Min, Max , F
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.views.generic import TemplateView

from .models import Product, Category
from .forms import CategoryForm, ProductForm, LoginForm


class ExampleView(View):
    http_method_names = ["get"]

    def get(request, *args, **kwargs):
        return HttpResponse("BCV")

# Create your views here.
@user_passes_test(lambda u: u.is_superuser)
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
        product = Product.objects.get(id=id)
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


class ProductView(View):
    http_method_names = ["get", "post"]

    def get(self, request):
        form = ProductForm()
        context = {"form": form}
        return render(request, "create_product.html", context=context)
    
    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = ProductForm()
            return redirect("home")
        context = {"form": form}
        return render(request, "create_product.html", context=context)


def register(request):
    if request.method == "GET":
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "register.html", context=context)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form = UserCreationForm()
            return redirect("home")
        context = {"form": form}
        return render(request, "register.html", context=context)


def login_user(request):
    if request.method == "GET":
        form = LoginForm()
        context = {"form": form}
        return render(request, "login.html", context=context)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("home")
        context = {"form": form}
        return render(request, "login.html", context=context)


def logout_user(request):
    logout(request)
    return redirect("home")


class AboutUs(TemplateView):
    template_name = "about_us.html"