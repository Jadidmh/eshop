from django.contrib import messages
from django.db.models.aggregates import Count, Max, Sum
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from .filters import OrderFilter
from order.models import OrderItem
from django.shortcuts import redirect
from product.models import Shop, Product
from order.models import Order



# Create your views here.


class OrderList(LoginRequiredMixin, DetailView):
    template_name = 'orderList.html'
    login_url = ''
    model = Shop

    def get_queryset(self, *arg, **kwargs):
        return Shop.UnDeleted.filter(slug=self.kwargs['slug'], seller=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        filter_order = OrderFilter(self.request.GET, queryset=Order.objects.filter(
            orderitem__product__shop__slug=self.kwargs['slug']).annotate(Count('id')).order_by('-created_at'))
        context['filter'] = filter_order
        return context


class ProductList(LoginRequiredMixin, DetailView):
    template_name = 'productList.html'
    login_url = ''
    model = Shop

    def get_queryset(self, *arg, **kwargs):
        return Shop.UnDeleted.filter(slug=self.kwargs['slug'], seller=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.filter(shop=context['shop'])
        return context


class OrderDetail(LoginRequiredMixin, DetailView):
    template_name = 'orderDetail.html'
    login_url = ''
    model = Order

    def get_queryset(self, *arg, **kwargs):
        return Shop.UnDeleted.filter(slug=self.kwargs['slug'], seller=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.UnDeleted.filter(seller=self.request.user).order_by('id')
        context['order_list'] = Order.objects.filter(id=self.kwargs['id'], orderitem__product__shop__slug=self.kwargs['slug']).annotate(Count('id')).order_by('-created_at')
        context['orderitem_list'] = OrderItem.objects.filter(order_id=self.kwargs['id'], product__shop__slug=self.kwargs['slug'])
        shop_total_price = 0
        shop_total_quantity = 0
        a = 0
        for item in context['orderitem_list']:
            shop_total_price += item.total_item_price
            shop_total_quantity += item.quantity
            a += item.discount
        context['shop_total_price'] = shop_total_price
        context['shop_total_quantity'] = shop_total_quantity
        context['a'] = a / len(context['orderitem_list'])

        return context


class OrderEditstatus(LoginRequiredMixin, View):
    login_url = '/'
    model = Order

    def get(self, request, *args, **kwargs):
        obj = self.model.objects.filter(pk=self.kwargs['pk'])
        obj = Order.objects.filter(pk=self.kwargs['pk']).first()
        if obj.status == 'CH':
            self.model.objects.filter(pk=self.kwargs['pk']).update(status= 'CO')
        elif obj.status == 'CANCELED':
            self.model.objects.filter(pk=self.kwargs['pk']).update(status= 'CH')
        else:
            self.model.objects.filter(pk=self.kwargs['pk']).update(status= 'CA')
            messages.info(request, f"سفارش شماره {obj.id} لغو شد." )
        return redirect('order_list_url', self.kwargs['slug'])

class OrderEditPayment(LoginRequiredMixin, View):
    login_url = '/'
    model = Order

    def get(self, request, *args, **kwargs):
        obj = Order.objects.filter(pk=self.kwargs['pk']).first()
        if obj.is_payment == False:
            self.model.objects.filter(pk=self.kwargs['pk']).update(is_payment = True)
        return redirect('order_list_url', self.kwargs['slug'])

class ClientList(LoginRequiredMixin, DetailView):
    template_name = 'clientList.html'
    login_url = '/'
    model = Shop

    def get_queryset(self, *arg, **kwargs):
        return Shop.UnDeleted.filter(slug=self.kwargs['slug'], seller=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.UnDeleted.filter(seller=self.request.user).order_by('id')
        context['client_order'] = Order.objects.filter(shop=context['shop']
                ).values('client', 'client__phone', 'client__image', 'client__username').annotate(
                                                                        last_order=Max('updated_at'),
                                                                        order_count=Count('id'),
                                                                        purchase_price=Sum('total_price'),
                                                                        purchase_quantity=Sum('total_quantity')
                                                                        ).order_by()
        return context



class OrderChart(LoginRequiredMixin, DetailView):
    template_name = 'orderChart.html'
    login_url = '/'
    model = Shop

    def get_queryset(self, *arg, **kwargs):
        return Shop.UnDeleted.filter(slug=self.kwargs['slug'], seller=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_list'] = Shop.UnDeleted.filter(seller=self.request.user).order_by('id')
        context['chart_data'] = Order.objects.filter(shop=context['shop']
                ).values('client__username').annotate(
                                                    order_count=Count('id'),
                                                    purchase_price=Sum('total_price'),
                                                    purchase_quantity=Sum('total_quantity')
                                                    ).order_by()
        context['barchart_data'] = Order.objects.filter(shop=context['shop']
                ).values('created_at__date').annotate(
                                                    order_count=Count('id'),
                                                    purchase_price=Sum('total_price'),
                                                    purchase_quantity=Sum('total_quantity')
                                                    ).order_by('created_at__date')
        context['barchart_data2'] = Order.objects.filter(shop=context['shop']
                ).values('created_at__month').annotate(
                                                    order_count=Count('id'),
                                                    purchase_price=Sum('total_price'),
                                                    purchase_quantity=Sum('total_quantity')
                                                    ).order_by('created_at__month')
        context['barchart_data3'] = Order.objects.filter(shop=context['shop']
                ).values('created_at__year').annotate(
                                                    order_count=Count('id'),
                                                    purchase_price=Sum('total_price'),
                                                    purchase_quantity=Sum('total_quantity')
                                                    ).order_by('created_at__year')
        return context

