from django.urls import path
from .views import CreateProduct, EditProduct, CreateShop, DeleteShop, ShopDetail, EditShop


urlpatterns = [
    path('shop/detail/<slug:slug>/', ShopDetail.as_view(), name='shopDetail'),
    path('create/shop/', CreateShop.as_view(), name='createShop'),
    path('edit/shop/<slug:slug>/', EditShop.as_view(), name='editShop'),
    path('delete/shop/<slug:slug>/', DeleteShop.as_view(), name='deleteShop'),
    path('create/product/<slug:slug>/', CreateProduct.as_view(), name='createProduct'),
    path('edit/product/<slug:slug>/', EditProduct.as_view(), name='editProduct'),

]