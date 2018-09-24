from rest_framework import generics, permissions
from shop_api import serializers
from shop_api.models import Shop, Order, Product, LineItem
from shop_api.permissions import IsResourceOwnerOrReadOnly, IsShopOwnerOrReadOnly, IsOrderOwnerOrShopOwnerReadOnly


class ShopAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating shops

    get:
    Returns a list of all the available shops

    post:
    Creates a new shop with the authenticated user as the owner.
    """

    serializer_class = serializers.ShopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Shop.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ShopRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating and destroying shops

    get:
    Returns the detail for the shop with the provided id

    put:
    Fully updates the shop with the provided id.
    All data fields in the request body are required, see the model below for details.

    The authenticated user must be the shop owner to perform this operation.

    patch:
    Partially updates the shop with the provided id.
    All data fields in the request body are optional, see the model below for details.
    The authenticated user must be the shop owner to perform this operation.

    delete:
    Deletes the shop with the provided id.

    The authenticated user must be the shop owner to perform this operation.
    """

    lookup_field = 'pk'
    serializer_class = serializers.ShopSerializer
    permission_classes = [IsResourceOwnerOrReadOnly]

    def get_queryset(self):
        return Shop.objects.all()


class ProductAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating products belonging to a shop

    get:
    Returns a list of all the available products for the shop with id=shop_id

    post:
    Creates a new product for the shop with id=shop_id.
    The authenticated user must be the shop owner to perform this action.
    """

    serializer_class = serializers.ProductSerializer
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
    """
    API view for retrieving, updating and destroying products belonging to a shop

    get:
    Returns the detail for the product with the provided id

    put:
    Fully updates the product with the provided id.
    All data fields in the request body are required, see the model below for details.
    The authenticated user must be the shop owner to perform this operation.

    patch:
    Partially updates the product with the provided id.
    All data fields in the request body are optional, see the model below for details.
    The authenticated user must be the shop owner to perform this operation.

    delete:
    Deletes the product with the provided id.
    The authenticated user must be the shop owner to perform this operation.
    """

    lookup_field = 'pk'
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        if shop_id is None:
            return Product.objects.none()

        shop_object = Shop.objects.get(pk=shop_id)
        return shop_object.products.all()


class OrderAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating orders belonging to a shop

    get:
    Returns a list of all the orders for the shop with id=shop_id

    post:
    Creates a new order for the shop with id=shop_id.
    The authenticated user will be the owner of the order that's created
    """

    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        if shop_id is None:
            return Order.objects.none()

        shop_object = Shop.objects.get(pk=shop_id)
        return shop_object.orders.all()

    def perform_create(self, serializer):
        shop_id = self.kwargs.get('shop_id')
        shop_object = Shop.objects.get(pk=shop_id)
        serializer.save(shop=shop_object, client=self.request.user)


class OrderRUDView(generics.RetrieveDestroyAPIView):
    """
    API view for retrieving, updating and destroying orders belonging to a shop.

    get:
    Returns the detail for the order with the provided id.

    delete:
    Deletes the order with the provided id.
    The authenticated user must be the order owner to perform this operation.
    """

    lookup_field = 'pk'
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsResourceOwnerOrReadOnly]

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        if shop_id is None:
            return Order.objects.none()

        shop_object = Shop.objects.get(pk=shop_id)
        return shop_object.orders.all()


class LineItemAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating line items belonging to an order

    get:
    Returns a list of all the line items for the order with id=order_id.
    The authenticated user must be order owner or shop owner to perform this action.

    post:
    Creates a new line item for the order with id=order_id.
    The authenticated user must be order owner to perform this action.
    """

    serializer_class = serializers.LineItemSerializer
    permission_classes = [IsOrderOwnerOrShopOwnerReadOnly]

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        if order_id is None:
            return LineItem.objects.none()

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
    """
    API view for retrieving, updating and destroying line items belonging to an order.

    get:
    Returns the detail for the line item with the provided id.
    The authenticated user must be the order or shop owner to perform this operation.

    put:
    Fully updates the line item with the provided id.
    All data fields in the request body are required, see the model below for details.
    The authenticated user must be the order owner to perform this operation.

    patch:
    Partially updates the line item with the provided id.
    All data fields in the request body are optional, see the model below for details.
    The authenticated user must be the order owner to perform this operation.

    delete:
    Deletes the line item with the provided id.
    The authenticated user must be the order owner to perform this operation.
    """

    serializer_class = serializers.LineItemUpdateSerializer
    permission_classes = [IsOrderOwnerOrShopOwnerReadOnly]

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        if order_id is None:
            return LineItem.objects.none()

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
