from django.contrib import admin
from catalog.models import (Category, Brand, Discount, Promo, Product, ProductImage, Cashback, Cart, Order,
                            OrderProductsM2M)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('article', 'brand', 'name', 'price')
    search_fields = ('article', 'name', 'category__name')


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Discount)
admin.site.register(Promo)
admin.site.register(ProductImage)
admin.site.register(Cashback)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)

