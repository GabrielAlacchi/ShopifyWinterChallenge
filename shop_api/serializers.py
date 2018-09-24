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
    order = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = LineItem
        fields = ('id', 'order', 'product', 'quantity', 'price')

    def validate_product(self, product):
        order_id = self.context['request'].parser_context['kwargs'].get('order_id')
        order = Order.objects.get(pk=order_id)

        if order.shop != product.shop:
            raise serializers.ValidationError("This shop does not sell this product: %s" % product)

        return product


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
    total = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ('id', 'client', 'shop', 'total', 'line_items')
