from django.conf.urls import url
from shop_api import views
from django.views.generic.base import RedirectView


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'$', RedirectView.as_view(url='shops/')),
    url(r'shops/$', views.ShopAPIView.as_view(), name='shops-listcreate'),
    url(r'shops/(?P<pk>\d+)/$', views.ShopRUDView.as_view(), name='shops-rud'),
    url(r'shops/(?P<shop_id>\d+)/products/$', views.ProductAPIView.as_view(), name='products-listcreate'),
    url(r'shops/(?P<shop_id>\d+)/products/(?P<pk>\d+)/$', views.ProductRUDView.as_view(), name='products-rud'),
    url(r'shops/(?P<shop_id>\d+)/orders/$', views.OrderAPIView.as_view(), name='orders-listcreate'),
    url(r'shops/(?P<shop_id>\d+)/orders/(?P<pk>\d+)/$', views.OrderRUDView.as_view(), name='orders-rud'),
    url(r'shops/(?P<shop_id>\d+)/orders/(?P<order_id>\d+)/lineitems/$', views.LineItemAPIView.as_view(), name='lineitems-listcreate'),
    url(r'shops/(?P<shop_id>\d+)/orders/(?P<order_id>\d+)/lineitems/(?P<pk>\d+)/$', views.LineItemRUDView.as_view(), name='lineitems-rud'),
]
