from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from order.models import OrderItem
from django.shortcuts import get_object_or_404
from product.models import Shop, Product
from order.models import Order
from .serializers import OrderItemCreateSerializer, OrderItemSerializer, OrderSerializer
from rest_framework.response import Response

class CreateOrderView(generics.ListCreateAPIView):
    model = OrderItem
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *arg, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        order = get_object_or_404(Order, shop=shop, client=self.request.user, is_payment=False)
        return OrderItem.objects.filter(order=order)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderItemSerializer
        elif self.request.method == 'POST':
            return OrderItemCreateSerializer

    def create(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        product_id = request.data['product']
        if product_id:
            product = get_object_or_404(Product, id=product_id, shop__slug=self.kwargs['slug'])
            if product.stock > 0:
                if product.is_active == True:
                    try:
                        order = Order.objects.get(shop=shop, client=self.request.user, is_payment=False)
                    except:
                        order = Order.objects.create(shop=shop, client=self.request.user)
                    request.data['order'] = order.id

                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return Response({'Error': 'This product is out of order'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Error': 'Enter you product'}, status=status.HTTP_404_NOT_FOUND)



class DeleteOrderView(generics.DestroyAPIView):
    model = OrderItem
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemSerializer

    def get_queryset(self, *arg, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        order = Order.objects.get(shop=shop, client=self.request.user, is_payment=False)
        return OrderItem.objects.filter(order=order)
    
    def delete(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        order = Order.objects.get(shop=shop, client=self.request.user, is_payment=False)
        orderitem = OrderItem.objects.filter(order=order)
        self.destroy(request, *args, **kwargs)
        if orderitem.count() == 0:
            order.delete()
            return Response({'Massage': 'Your basket is empty.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'Massage': 'Item deleted.'}, status=status.HTTP_204_NO_CONTENT)


class PayOrderView(generics.UpdateAPIView):
    http_method_names = ['put',]
    model = Order
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self, *arg, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        order = Order.objects.get(shop=shop, client=self.request.user, is_payment=False)
        return order
    
    def put(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        try:
            order = Order.objects.get(shop=shop, client=self.request.user, is_payment=False)
        except:
            return Response({'Error': 'No order to pay'}, status=status.HTTP_204_NO_CONTENT)
        if order.id == self.kwargs['pk']:
            order.is_payment=True
            order.save()
            return Response({'Success': 'Payment done'}, status=status.HTTP_202_ACCEPTED)
        return Response({'Error': 'Incorrect order id'}, status=status.HTTP_400_BAD_REQUEST)


class UnpaidOrderView(generics.ListAPIView):
    model = Order
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self, *arg, **kwargs):
        return Order.objects.filter(client= self.request.user, is_payment=False)


class PaidOrderView(generics.ListAPIView):
    model = Order
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self, *arg, **kwargs):
        return Order.objects.filter(client= self.request.user, is_payment=True)