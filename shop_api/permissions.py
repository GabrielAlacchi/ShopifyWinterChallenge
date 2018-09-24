from rest_framework import permissions
from shop_api.models import Shop, Order


class IsResourceOwnerOrReadOnly(permissions.BasePermission):

    """
    This permission class ensures that only the owner of a resource has the
    permission to modify its contents. It allows reading permissions
    to non-owners.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsShopOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        shop_id = view.kwargs.get('shop_id')

        if shop_id is None:
            return True

        return Shop.objects.get(pk=shop_id).owner == request.user


class IsOrderOwnerOrShopOwnerReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        order_id = view.kwargs.get('order_id')
        shop_id = view.kwargs.get('shop_id')

        if shop_id is None or order_id is None:
            return True

        is_order_owner = Order.objects.get(pk=order_id).owner == request.user
        is_shop_owner = Shop.objects.get(pk=shop_id).owner == request.user

        if request.method in permissions.SAFE_METHODS:
            return is_order_owner or is_shop_owner
        else:
            return is_order_owner
