from rest_framework import serializers
from catalog.models import Category, Cashback, Discount, Promo, Product, ProductImage, Order, OrderProductsM2M
from datetime import date


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
        fields = ('image',)


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


class AddProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()


class DiscountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('percent',)


class ProductInCartSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()
    discounts = DiscountsSerializer(source='discount', many=True)

    class Meta:
        model = Product
        fields = ('name', 'price', 'amount', 'discounts')


class CartSerializer(serializers.Serializer):
    products = ProductInCartSerializer(many=True)


class DeleteProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


class OrderProductsM2MSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProductsM2M
        fields = ('product', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    promo = serializers.CharField(max_length=300, write_only=True)
    products = OrderProductsM2MSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ('id', 'created', 'total_price', 'status',
                  'payment_status', 'delivery_method', 'notification_time', 'products', 'promo')
        read_only_fields = ('created', 'status', 'payment_status', 'total_price')

    def create(self, validated_data):
        products = validated_data.pop('products')
        promo_name = validated_data.pop('promo')
        promo = Promo.objects.filter(name=promo_name).first()

        total_sum = 0

        for item in products:
            product = item.get('product')
            amount = item.get('amount')
            discounts = Discount.objects.prefetch_related('product_set').filter(product__id=product.id)
            current_date = date.today()
            discount_percents = []
            for disc in discounts:
                delta = current_date - disc.exp_date
                if delta.days <= 0:
                    discount_percents.append(disc.percent)
            total_discount = sum(discount_percents) if len(discount_percents) > 0 else 0
            total_sum += (product.price * (100 - total_discount) / 100) * amount

        if promo.is_cumulative:
            total_sum *= ((100 - promo.percent) / 100)

        user = self.context['request'].user
        order = Order.objects.create(total_price=total_sum, user=user, **validated_data)

        for product in products:
            OrderProductsM2M.objects.create(order=order, **product)

        return order
