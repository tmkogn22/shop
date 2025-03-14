from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from catalog.models import Category
from catalog.serializers import CategorySerializer


class CategoryListView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
