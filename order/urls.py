from django.urls import path
from .views import ClientList, OrderChart, OrderEditstatus, OrderList, ProductList, OrderDetail, OrderEditPayment


urlpatterns = [
    path('order/list/<slug:slug>/', OrderList.as_view(), name='order_list_url'),
    path('product/list/<slug:slug>/', ProductList.as_view(), name='product_list_url'),
    path('order/detail/<slug:slug>/<int:id>/', OrderDetail.as_view(), name='order_detail_url'),
    path('order/edit/status/<slug:slug>/<int:pk>/', OrderEditstatus.as_view(), name='order_status_url'),
    path('order/edit/pymant/<slug:slug>/<int:pk>/', OrderEditPayment.as_view(), name='order_payment_url'),
    path('client/list/<slug:slug>/', ClientList.as_view(), name='client_list_url'),
    path('chart/<slug:slug>/', OrderChart.as_view(), name='order_chart_url'),

]