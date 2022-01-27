from django.urls import path
from .viewApis import ClientRegisterView, GetTokenForLoginView, ClientProfileView, ActivateUserPhone, GenerateOtpForLogin, LoginWithOtp, GenerateOtpForActivate
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('client/register/', ClientRegisterView.as_view(), name='clientRegister'),
    path('client/login/', GetTokenForLoginView.as_view(), name='clientLogin'),
    path('client/login/refresh/', TokenRefreshView.as_view(), name='clientLogin_refresh'),
    path('client/profile/', ClientProfileView.as_view(), name='clientProfile'),
    path('client/activate/phone/', ActivateUserPhone.as_view() ,name="activate_user"),
    path('client/activate/generate_otp/phone/', GenerateOtpForActivate.as_view() ,name="generate_otp_activate_user"),
    path('client/generate_otp/' , GenerateOtpForLogin.as_view() , name="generate_otp_login"),
    path('client/otp_login/' , LoginWithOtp.as_view() , name="login_with_otp")
]
