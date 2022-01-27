from django.contrib.auth.views import LoginView, LogoutView
from .forms import SellerRegisterForm, SellerLoginForm, UpdateProfileSellerForm
from product.models import Shop
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from .models import User




# Create your views here.


class SellerLogin(LoginView):
    template_name = 'sellerLogin.html'
    form_class = SellerLoginForm

    def get(self, request):
        if request.user.is_authenticated:
            shop = Shop.UnDeleted.filter(seller=self.request.user).first()
            if shop:
                return redirect('shopDetail', slug=shop.slug)
            return redirect('createShop')
        form = SellerLoginForm()
        return render(request, 'sellerLogin.html', {'form': form})
    
    def post(self, request):
        form = SellerLoginForm(request.POST)
        print(form)
        if form.is_valid():
            user = authenticate(phone=form.cleaned_data['phone'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_seller and user.is_active:
                        login(request, user)
                        shop = Shop.UnDeleted.filter(seller=self.request.user).first()
                        messages.success(request, "با موفقیت وارد شدید" )
                        if shop:
                            return redirect('shopDetail', slug=shop.slug)
                        return redirect('createShop')
                messages.info(request, "شما فروشنده نیستید یا حسابتان به حالت تعلیق درآمده است." )
                return redirect('sellerLogin')

        messages.info(request, "ورود ناموفق کاربر نامعتبر" )
        return redirect('sellerLogin')


class SellerLogout(LogoutView):
    def get(self, request):
        logout(request)
        messages.info(request, "با موفقیت خارج شدید" )
        return redirect('sellerLogin')


class SellerRegister(CreateView):
    template_name = 'sellerRegister.html'
    success_url =reverse_lazy("sellerLogin")
    form_class = SellerRegisterForm
    success_message = "شما با موفقیت ثبت نام کردید"

    def get(self, request):
        if request.user.is_authenticated:
            slug = Shop.UnDeleted.filter(seller=self.request.user).first().slug
            messages.success(request, "شما قبلا وارد شده اید." )
            return redirect('shopDetail', slug=slug)
        form = SellerRegisterForm()
        return render(request, 'sellerRegister.html',{'form': form})
    
    def post(self, request):
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ثبت نام با موفقیت انجام شد." )
            return redirect('sellerLogin')
        messages.error(request, "ورودی نامعتبر !" )

        return redirect('sellerRegister')

class SellerProfile(LoginRequiredMixin, TemplateView):
    template_name = "admin_profile.html"
   

class UpdateSellerProfile(LoginRequiredMixin,UpdateView):
    template_name="update_profile_admin.html"
    success_url =reverse_lazy("user:adminProfile")
    form_class=UpdateProfileSellerForm
    model= User

    def get_object(self, queryset=None):
        return self.request.user