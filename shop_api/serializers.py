from rest_framework import serializers
from shop_api.models import Shop, Product, Order, LineItem


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ('id', 'name', 'owner')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'shop', 'name', 'description', 'price')


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'client', 'shop')


class LineItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = LineItem
        fields = ('id', 'product', 'order', 'quantity', 'price')
