from django import forms
from .models import Category, Product
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("__all__")


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)  