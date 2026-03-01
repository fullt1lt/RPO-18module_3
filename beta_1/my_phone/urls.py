from django.urls import path
from .views import home, hello, helloid, product_detail, form_view, product_form_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("home/", home, name="home"),
    path("hello/<str:name>", hello, name="hello_str"),
    path("helloid/<int:id>", helloid, name="hello_id"),
    path("product/<int:id>", product_detail, name="product_detail"),
    path("form-view/", form_view, name="form-view"),
    path("create-product/", product_form_view, name="create-product"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
