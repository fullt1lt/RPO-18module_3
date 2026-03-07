from django import forms
from .models import Category, Product
from django.contrib.auth import authenticate

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("__all__")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            self.user = authenticate(username=username, password=password)
            if not self.user:
                raise forms.ValidationError("Неверные имя пользователя или пароль")
        return cleaned_data