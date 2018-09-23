from rest_framework import serializers
from shop_api.models import Shop, Product, Order, LineItem


class ShopSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Shop
        fields = ('id', 'name', 'owner', 'products')


class ProductSerializer(serializers.ModelSerializer):
    shop = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'shop', 'name', 'description', 'price')


class LineItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    price = serializers.ReadOnlyField()

    class Meta:
        model = LineItem
        fields = ('id', 'product', 'quantity', 'price')


class LineItemUpdateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    price = serializers.ReadOnlyField()

    class Meta:
        model = LineItem
        fields = ('id', 'product', 'quantity', 'price')


class OrderSerializer(serializers.ModelSerializer):
    shop = serializers.PrimaryKeyRelatedField(read_only=True)
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    line_items = LineItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ('id', 'client', 'shop', 'total', 'line_items')
