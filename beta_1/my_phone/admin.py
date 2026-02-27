from django.contrib import admin

from .models import Category, Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name","descriptions", "price")
    search_fields = ("name", "price", "category__name")
    list_filter = ("price", "name")
    fieldsets = (
        ("Main info", {"fields": ("name", "descriptions","category")}),
        ("Price info", {"fields" : ("price", "image")})
        )
    ordering = ("id",)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
