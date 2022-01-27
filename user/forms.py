from django import forms
from django.forms import TextInput
from django.forms import Form
from django.forms.widgets import EmailInput
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy


class SellerRegisterForm(UserCreationForm):

    password1 = forms.CharField(
        label=gettext_lazy("رمز عبور"), strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور', 'autocomplete': 'new-password',
                                        'class':'form-control bg-dark text-warning', 'id': "password-field",}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label=gettext_lazy("تایید رمز عبور"), strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control  bg-dark text-warning',
                                        'id': "password-field2 bg-dark text-warning", 'placeholder': 'تایید رمز عبور', }),

        help_text=gettext_lazy("برای تایید همان رمز عبور قبلی را وارد کنید."),
    )

    class Meta:

        model = User
        fields = ("phone", "username", "email", "password1", "password2")
        widgets = {
            'phone': TextInput(attrs={'class':'form-control bg-dark text-warning', 'placeholder': "شماره تلفن"}),

            'username': TextInput(attrs={'class':'form-control bg-dark text-warning', 'placeholder': 'نام کاربری'}),
        
            'email': EmailInput(attrs={'class':'form-control bg-dark text-warning', 'placeholder': 'ایمیل'}),
        }

    def save(self, commit=True):
        user = super(SellerRegisterForm, self).save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.is_seller = True
        if commit:
            user.save()
        return user


class SellerLoginForm(Form):
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "تلفن یا نام کاربری یا ایمیل را وارد کنید (فقط یکی)",
                                      'class':'form-control bg-dark text-warning', 'autofocus': True}))
    
    password = forms.CharField(strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور', 'class':'form-control bg-dark text-warning', 
                                          'id': "password-field",'autocomplete': 'current-password'}),)

class UpdateProfileSellerForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control mt-2 text-warning bg-dark h5'}), label='نام کاربری')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control mt-2 text-warning bg-dark h5'}), label='ایمیل')
    phone = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control mt-2 text-warning bg-dark h5'}), label='تلفن همراه')
    image = forms.FileField(widget=forms.FileInput(attrs={'class' : 'form-control mt-2 text-warning bg-dark h5'}), label='عکس کاربر')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control mt-2 text-warning bg-dark h5'}), label='نام')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control mt-2 text-warning bg-dark h5'}), label='نام خانوادگی')


    class Meta:
        model=User
        fields=["username" , "email" , "phone" , "image" , "first_name" ,"last_name"]