from rest_framework import generics, permissions
from shop_api.models import Shop, Order
from shop_api.serializers import ShopSerializer, ProductSerializer, OrderSerializer, LineItemSerializer
from shop_api.permissions import IsResourceOwnerOrReadOnly, IsShopOwnerOrReadOnly, IsOrderOwner


class ShopAPIView(generics.ListCreateAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Shop.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ShopRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ShopSerializer
    permission_classes = [IsResourceOwnerOrReadOnly]

    def get_queryset(self):
        return Shop.objects.all()


class ProductAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsShopOwnerOrReadOnly]

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        shop_object = Shop.objects.get(pk=shop_id)
        return shop_object.products.all()

    def perform_create(self, serializer):
        shop_id = self.kwargs.get('shop_id')
        shop_object = Shop.objects.get(pk=shop_id)
        serializer.save(shop=shop_object)


class ProductRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = ProductSerializer

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        shop_object = Shop.objects.get(pk=shop_id)
        return shop_object.products.all()


class OrderAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        shop_object = Shop.objects.get(pk=shop_id)
        return shop_object.orders.all()

    def perform_create(self, serializer):
        shop_id = self.kwargs.get('shop_id')
        shop_object = Shop.objects.get(pk=shop_id)
        serializer.save(shop=shop_object, client=self.request.user)


class OrderRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = OrderSerializer
    permission_classes = [IsResourceOwnerOrReadOnly]

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        shop_object = Shop.objects.get(pk=shop_id)
        return shop_object.orders.all()


class LineItemAPIView(generics.ListCreateAPIView):
    serializer_class = LineItemSerializer
    permission_classes = [IsOrderOwner]

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        order_object = Order.objects.get(pk=order_id)
        return order_object.line_items.all()

    def perform_create(self, serializer):
        order_id = self.kwargs.get('order_id')
        order_object = Order.objects.get(pk=order_id)

        product_object = serializer.validated_data.get('product')
        serializer.save(order=order_object, price=product_object.price)

        order_object.update_total()
        order_object.save()


class LineItemRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LineItemSerializer
    permission_classes = [IsOrderOwner]

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        order_object = Order.objects.get(pk=order_id)
        return order_object.line_items.all()

    def perform_update(self, serializer):
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(pk=order_id)
        serializer.save()

        order.update_total()
        order.save()

    def perform_destroy(self, instance):
        order = instance.order
        instance.delete()

        order.update_total()
        order.save()
