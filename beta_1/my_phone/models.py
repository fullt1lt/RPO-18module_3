from django.db import models
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=50)
    descriptions = models.TextField(null=True, blank=True, default="123")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to='products/', null=True)
    category = models.ManyToManyField(
        "Category", related_name="product"
    )
    def __str__(self):
        return f"{self.id} - {self.name}"

    def clean(self):
        super().clean()
        
        if self.price < 0:
            raise ValidationError("Цена не может быть отрицательной!!!")



class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"