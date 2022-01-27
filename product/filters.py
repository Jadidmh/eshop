import django_filters

from .models import Product, Shop


class ShopListFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name='type')

    class Meta:
        model = Shop
        fields = ['type']


class ShopProductsFilter(django_filters.FilterSet):
    tag = django_filters.NumberFilter(field_name='tag')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    available = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = Product
        fields = ['tag', 'price__lt', 'price__gt', 'available']
