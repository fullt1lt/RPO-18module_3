from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum, Avg, Min, Max , F
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.core.cache import cache
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin


from .models import Product, Category
from .forms import CategoryForm, ProductForm, LoginForm


class AdminUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class HomeRedirectView(RedirectView):
    url = reverse_lazy("home")


class ExampleView(View):
    http_method_names = ["get"]

    def get(request, *args, **kwargs):
        return HttpResponse("BCV")


class HomeListView(ListView):
    http_method_names = ["get", "post"]
    model = Product
    template_name = "home.html"
    context_object_name = "products"
    paginate_by = 1

    def get_queryset(self):
        return cache.get_or_set("products", Product.objects.filter(price__lte=25000).order_by("-price", "name"), timeout=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    template_name = "product_detail.html"
    model = Product
    context_object_name = 'product'
    pk_url_kwarg = "id"


def hello(request, name):
    name = name.upper()
    context = {
        "name": name
    }
    return render(request, "hello.html", context)

def helloid(request, id):
    return HttpResponse(f"Hello {id}!!!")


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "form.html"
    success_url = '/home'
    
    def form_valid(self, form):
        if form.cleaned_data["name"].startswith('a'):
            form.add_error("name", "Error!!!")
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_initial(self):
        return {
            "name": "Default"
        }

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


class MyLoginView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy("home")


class AboutUs(TemplateView):
    template_name = "about_us.html"
    extra_context = {
        "title2": "Python",
        "products" : Product.objects.all()
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme = self.request.COOKIES.get("theme")
        product = Product.objects.all().first()
        key = self.request.session.get("temp", "567")
        print(key)
        context["title"] = "Hello!!!"
        context["product"] = product
        context["theme"] = theme
        context["key"] = key

        return context

    def post(self, request, *args, **kwargs):
        theme = request.POST.get("theme")

        request.session["temp"] = "123"
        response = redirect(request.path)

        if theme:
            response.set_cookie(
                key="theme",
                value=theme,
                max_age=60 * 60 * 24,
                httponly=True,
                samesite="Lax",
            )

        return response


class ProductDeleteView(DeleteView):
    model = Product
    pk_url_kwarg = "id"
    success_url = "/home"
