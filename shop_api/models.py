from django.db import models
from django.contrib.auth.models import User


# Shopify Challenge Models


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')

    def __str__(self):
        return self.name


class Product(models.Model):
    """

    """
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        return self.name

    @property
    def owner(self):
        return self.shop.owner


class Order(models.Model):
    # Don't delete the order if the user deletes their account for accounting purposes
    client = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', null=True)

    # One to one relation with a shop
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=19, decimal_places=2, default=0)

    def __str__(self):
        return 'Order: ' + str(self.id)

    def update_total(self):
        self.total = sum(item.price * item.quantity for item in self.line_items.all())

    @property
    def owner(self):
        return self.client


class LineItem(models.Model):
    """
    Association class between Product and Order
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='line_items')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='line_items')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        return self.product.name + ' x' + str(self.quantity)

    @property
    def owner(self):
        return self.order.owner
