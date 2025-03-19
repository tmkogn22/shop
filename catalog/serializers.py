from rest_framework import serializers
from catalog.models import Category, Cashback, Discount, Promo, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CashbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cashback
        fields = ('id', 'percent', 'limit')


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('id', 'name', 'start_date', 'exp_date', 'percent')


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ('id', 'name', 'percent', 'is_cumulative')


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductImage
        fields = ('image', )


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source='productimage_set')

    class Meta:
        model = Product
        fields = ('id', 'article', 'name', 'price', 'images')


class DiscountProductsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    article = serializers.CharField()
    discount_percent = serializers.IntegerField()
