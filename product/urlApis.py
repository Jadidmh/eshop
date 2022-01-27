from django.urls import path
from .viewApis import ShopListView, ShopProductsView, ShopTypesView


urlpatterns = [
    path('confirmed/', ShopListView.as_view(), name='shopConfirmed'), # SU HY VS FS OS CS
    path('type/', ShopTypesView.as_view(), name='shopTypes'),
    path('<slug:slug>/product/', ShopProductsView.as_view(), name='shopProducts'), #shop.slug
]