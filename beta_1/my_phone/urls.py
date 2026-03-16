from django.urls import path, include
from .views import (
    hello,
    helloid,
    ProductView,
    register,
    ExampleView,
    AboutUs,
    HomeListView,
    ProductDetailView,
    CategoryCreateView,
    ProductDeleteView,
    HomeRedirectView,
    MyLoginView,
)
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("home/", HomeListView.as_view(), name="home"),
    path("hello/<str:name>", hello, name="hello_str"),
    path("helloid/<int:id>", helloid, name="hello_id"),
    path("product/<int:id>", ProductDetailView.as_view(), name="product_detail"),
    path("form-view/", CategoryCreateView.as_view(), name="form-view"),
    path("create-product/", ProductView.as_view(), name="create-product"),
    path("register/", register, name="register"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page = "home"), name="logout"),
    path("example/", ExampleView.as_view(), name="example"),
    path("about-us/", AboutUs.as_view(), name="about-us"),
    path(
        "product/<int:id>/delete/", ProductDeleteView.as_view(), name="delete_product"
    ),
    path("", HomeRedirectView.as_view(), name="home_redirect"),
    ## API
    path("api/", include("my_phone.api.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
