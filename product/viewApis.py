from rest_framework import generics
from .filters import ShopListFilter, ShopProductsFilter
from .models import Shop, Product
from rest_framework.permissions import IsAuthenticated
from .serializers import ShopListSerializer, ShopTypesSerializer, ProductSerializer

class ShopListView(generics.ListAPIView):
    filterset_class = ShopListFilter
    queryset = Shop.UnDeleted.filter(is_confirmed=True)
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopListSerializer


class ShopTypesView(generics.ListAPIView):
    queryset = Shop.UnDeleted.filter(is_confirmed=True).distinct('type')
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopTypesSerializer


class ShopProductsView(generics.ListAPIView):
    filterset_class = ShopProductsFilter
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(shop__slug=self.kwargs['slug'], shop__is_confirmed=True)