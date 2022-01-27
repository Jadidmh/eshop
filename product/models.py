from django.db import models
from user.models import User
from .managers import UnDeletedShop, DeletedShop
import random
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator
from django.utils.html import format_html




# Create your models here.


class Shop(models.Model):
    SUPERMARKET = "SU"
    HYPERMARKET = "HY"
    VEGETABLESSTORE = "VS"
    FRUITSTORE = "FS"
    ORGANICSTORE = "OS"
    CONVENIENCESTORE = "CS"

    TYPE_CHOICES = (
        (SUPERMARKET, "سوپر مارکت"),
        (HYPERMARKET, "هایپر مارکت"),
        (VEGETABLESSTORE, "فروشگاه سبزیجات"),
        (FRUITSTORE, "میوه فروشی"),
        (ORGANICSTORE, "فروشگاه ارگانیک"),
        (CONVENIENCESTORE, "خواربارفروشی"),
    )
    slug = models.SlugField(max_length=60, blank=True, unique=True, verbose_name='اسلاگ')
    name = models.CharField(max_length=50, verbose_name='نام فروشگاه')
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=SUPERMARKET, verbose_name='نوع فروشگاه')
    address = models.TextField(verbose_name='آدرس')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='فروشنده')
    is_confirmed = models.BooleanField(default=False, verbose_name='تایید شده است')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده')

    objects = models.Manager()
    Deleted = DeletedShop()
    UnDeleted = UnDeletedShop()

    def __str__(self):
        return f'{self.seller.username} فروشگاه {self.id} با نام {self.name} برای یوزر '
    
    def random_number_generator(self):
        return '_' + str(random.randint(1000, 9999))

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name) + '_' + str.lower(self.type).replace(" ","_")
            while Shop.objects.filter(slug = self.slug):
                self.slug = slugify(self.name)
                self.slug += self.random_number_generator()
        return super().save(*args, **kwargs)


class Product(models.Model):
    slug = models.SlugField(blank=True, unique=True, verbose_name='اسلاگ')
    name = models.CharField(max_length=50, verbose_name='نام محصول')
    image = models.ImageField(upload_to='productImage/', verbose_name='عکس محصول')
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name='قیمت محصول')
    discount = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True, default=0, verbose_name='درصد تخفیف محصول')
    sales  = models.DecimalField(max_digits=12, decimal_places=2, blank=True, verbose_name='قیمت محصول')
    stock = models.PositiveIntegerField(default=0, blank=True, verbose_name='تعداد محصول')
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name='وزن محصول')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='به روز شده در')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='دسته بندی') 
    tag = models.ManyToManyField('Tag', blank=True, verbose_name='تگ')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_products', verbose_name='برای فروشگاه')
    is_active = models.BooleanField(default=False, verbose_name='فعال است')
    is_confirmed = models.BooleanField(default=False, verbose_name='تایید شده است')

    class Meta:
        ordering = ['-id']

    def random_number_generator(self):
        return '_' + str(random.randint(1000, 9999))

    def image_tag(self):
        return format_html('<img src="{}"  width="50" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.image)
            while Product.objects.filter(slug = self.slug):
                self.slug = slugify(self.image)
                self.slug += self.random_number_generator()
                
        if self.stock == 0:
            self.is_active = False
        if not self.sales:
            price = self.price
            self.sales = price - ((price * self.discount) /100 )
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='موضوع دسته بندی')

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=50,verbose_name='موضوع تگ')

    class Meta : 
        ordering = ['title',]
        
    def __str__(self):
        return self.title