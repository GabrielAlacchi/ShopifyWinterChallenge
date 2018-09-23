from django.contrib import admin
from shop_api.models import Shop, Product, Order, LineItem

# Register your models here.
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(LineItem)
