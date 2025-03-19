from django.shortcuts import render
from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from catalog.models import Category, Cashback, Discount, Promo, Product
from catalog.serializers import (CategorySerializer, CashbackSerializer, DiscountSerializer, PromoSerializer,
                                 ProductSerializer, DiscountProductsSerializer)


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
