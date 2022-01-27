from django import forms
from django.forms import ModelForm, Textarea, TextInput, models
from django.forms.widgets import CheckboxInput, ClearableFileInput, NumberInput, RadioSelect, Select, SelectMultiple
from .models import Product, Shop


class CreateShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'address', 'type')
        widgets = {
            'name': TextInput(attrs={'class':'form-control', 
                                    'placeholder': "نام فروشگاه خود را وارد کنید"}),

            'address': TextInput(attrs={'class':'form-control', 
                                    'placeholder': 'مثال تهران ، میدان تهران ، خیابان تهران ، پاساژ تهران ، طبقه اول ، واحد 5 '}),
            'type': forms.Select(attrs={'class':'form-select w-100'}),
        }


class CreateProductForm(ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class' : 'form-control mt-2 bg-dark text-warning border-0 my-2'}))

    class Meta:
        model = Product
        exclude = ['slug', 'created_at', 'updated_at', 'shop', 'is_confirmed']
        widgets = {
            'name': TextInput(attrs={'class':'form-control bg-dark text-warning border-0 my-2', 
                                    'placeholder': "نام محصول رو وارد کنید"}),
            
            'price': NumberInput(attrs={'class':'form-control bg-dark text-warning border-0 my-2', 
                                    'placeholder': 'قیمت محصول خود را وارد کنید'}),


            'discount': NumberInput(attrs={'class':'form-control bg-dark text-warning border-0 my-2', 
                                    'placeholder': 'Enter like: 0.15  - It is equal to 15%'}),

            'stock': NumberInput(attrs={'class':'form-control bg-dark text-warning border-0 my-2', 
                                    'placeholder': ''}),

            'weight': NumberInput(attrs={'class':'form-control bg-dark text-warning border-0 my-2', 
                                    'placeholder': '450 (gr)'}),

            'description': Textarea(attrs={'class':'form-control bg-dark text-warning border-0 my-2', 
                                    'placeholder': ""}),

            'category': Select(attrs={'class':'form-control bg-dark text-warning border-0 my-2', 
                                    'placeholder': ""}),

            'tag': SelectMultiple(attrs={'class':'form-control bg-dark text-warning border-0 my-2', 
                                    'placeholder': ""}),

            'is_active': CheckboxInput(attrs={'class':'form-check-input bg-dark text-warning border-0 my-2'}),
        }