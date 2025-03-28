from django.shortcuts import render
from django.db.models import F, Prefetch
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from catalog.models import Category, Cashback, Discount, Promo, Product, Cart
from catalog.serializers import (CategorySerializer, CashbackSerializer, DiscountSerializer, PromoSerializer,
                                 ProductSerializer, DiscountProductsSerializer, AddProductSerializer, CartSerializer,
                                 DeleteProductSerializer)


class CategoryListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CashbackView(APIView):
    def get(self, request):
        some_model_obj = Cashback.objects.all()
        serializer = CashbackSerializer(some_model_obj, many=True)
        return Response(serializer.data)


class DiscountListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class PromoListView(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer


class CategoryProductsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, category_id):
        queryset = Product.objects.filter(category__id=category_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class DiscountProducts(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, discount_id):
        queryset = Product.objects.prefetch_related('discount_set').filter(discount__id=discount_id
                                                                           ).values('name',
                                                                                    'price',
                                                                                    'article',
                                                                                    'id',
                                                                                    discount_percent=F(
                                                                                        'discount__percent'))
        serializer = DiscountProductsSerializer(queryset, many=True)
        return Response(serializer.data)


class CartView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        cart_item = Product.objects.prefetch_related(Prefetch('discount', queryset=Discount.objects.only('percent'))).filter(
            cart__user=user
        ).annotate(amount=F('cart__amount'))
        serializer = CartSerializer({'products': cart_item})

        return Response(serializer.data)

    def post(self, request):
        input_serializer = AddProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        product = Product.objects.get(id=input_serializer.data['product_id'])
        cart_item, _ = Cart.objects.get_or_create(user=request.user, product=product)

        if not cart_item.amount:
            cart_item.amount = input_serializer.data['amount']
        else:
            cart_item.amount += input_serializer.data['amount']

        cart_item.save()

        return Response()

    def delete(self, request):
        input_serializer = DeleteProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        product = Product.objects.get(id=input_serializer.data['product_id'])
        Cart.objects.get(user=request.user, product=product).delete()

        return Response()
