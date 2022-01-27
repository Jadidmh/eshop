from django.urls import path
from .views import SellerLogin, SellerLogout, SellerRegister, SellerProfile, UpdateSellerProfile


urlpatterns = [
    path('', SellerLogin.as_view(), name='sellerLogin'),
    path('seller/logout/', SellerLogout.as_view(), name='sellerLogout'),
    path('seller/register/', SellerRegister.as_view(), name='sellerRegister'),
    path('sellerprofile/' ,SellerProfile.as_view()  ,name="sellerProfile" ),
    path('sellerprofile/update/' ,UpdateSellerProfile.as_view()  ,name="updateSellerProfile" ),
]
