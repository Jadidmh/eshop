import django_filters
from django import forms
from order.models import Order

class OrderFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(widget=forms.SelectDateWidget(years=range(2020, 2020 + 10)),
    field_name='created_at', lookup_expr='gt')
    end_date = django_filters.DateFilter(widget=forms.SelectDateWidget(years=range(2020, 2020 + 10)),
    field_name='created_at', lookup_expr='lt')

    class Meta:
        model = Order
        fields = ['status', 'start_date', 'end_date']
