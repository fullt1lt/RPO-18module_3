from rest_framework import serializers
from my_phone.models import Product, Category


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    descriptions = serializers.CharField(required=False, allow_blank=True, default="123")
    price = serializers.DecimalField(decimal_places=2, max_digits=10)
    image = serializers.ImageField(required=False, allow_null=True)
    category = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        product.category.set(category_data)
        return product

    def update(self, instance, validated_data):
        category_data = validated_data.pop("category")
        instance.name = validated_data.get("name", instance.name)
        instance.descriptions = validated_data.get("descriptions", instance.descriptions)
        instance.price = validated_data.get("price", instance.price)
        instance.save()
        instance.category.set(category_data)
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name"]


class ProductModelSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    url_object = serializers.SerializerMethodField(read_only=True)
    category = CategorySerializer(many=True)
    class Meta:
        model = Product
        fields = ["name", "descriptions", "price", "image", "category", "url_object"]
        read_only_fields = ["id"]


    def get_url_object(self, obj):
        return f"/api/{obj.id}"


    def create(self, validated_data):
        category_data = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        product.category.set(category_data)
        return product


    def update(self, instance, validated_data):
        category_data = validated_data.pop("category")
        instance.name = validated_data.get("name", instance.name)
        instance.descriptions = validated_data.get("descriptions", instance.descriptions)
        instance.price = validated_data.get("price", instance.price)
        instance.save()
        instance.category.set(category_data)
        return instance
