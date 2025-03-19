from django.urls import path
from catalog.views import (CategoryListView, CashbackView, DiscountListView, PromoListView, CategoryProductsView,
                           DiscountProducts)



urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('cashback/', CashbackView.as_view(), name='cashback'),
    path('discounts/', DiscountListView.as_view(), name='discounts'),
    path('promos/', PromoListView.as_view(), name='promos'),
    path('categories/<int:category_id>/', CategoryProductsView.as_view(), name='category-products'),
    path('discounts/<int:discount_id>/', DiscountProducts.as_view(), name='discount-products')
]
