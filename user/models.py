from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy
from .managers import UserManager
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify
import random

# Create your models here.

class User(AbstractUser):

    email = models.EmailField(gettext_lazy('ایمیل'), unique=True)

    phone_regex = RegexValidator(regex=r'^09\d{9}$', message="شماره تلفن باید در قالب '09010944090' وارد شود.")

    phone = models.CharField(validators=[phone_regex], max_length=11, unique=True, verbose_name='تلفن همراه')

    username_regex = RegexValidator(regex = r'^[\w.+-]*[a-zA-Z][\w.+-]*\Z', message="نام کاربری باید حداقل یک حرف داشته باشد و @ پذیرفته نمی شود")
    
    username = models.CharField(gettext_lazy('نام کاربری'),max_length=150,unique=True,
        help_text=gettext_lazy('هشدار نام کاربری باید بین 1 تا 150 حرف باشد و (فقط از حروف، اعداد و . / + / - / _ استفاده شود)'),
        validators=[username_regex],
        error_messages={'unique': gettext_lazy("کاربری با آن نام کاربری از قبل وجود دارد."),},
    )

    image = models.ImageField(upload_to='user_image/', null=True, blank=True, verbose_name='عکس')

    is_client = models.BooleanField(gettext_lazy('مشتری هست'),default=False,
        help_text=gettext_lazy('مشخص می کند که آیا کاربر می تواند به عنوان مشتری وارد سیستم شود یا خیر.'),
    )

    is_seller = models.BooleanField(gettext_lazy('فروشنده هست'),default=False,
        help_text=gettext_lazy('مشخص می کند که آیا کاربر می تواند به عنوان فروشنده وارد سیستم شود یا خیر.'),
    )
    
    is_register=models.BooleanField(default=False)

    if phone:
        USERNAME_FIELD = 'phone'
        REQUIRED_FIELDS = [ 'username', 'email']
    elif email:
        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = [ 'username', 'phone']
    else:
        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = [ 'phone', 'email']
    
    objects = UserManager()

    def __str__(self):
        return f'{self.username} کاربر {self.id} با نام کاربری'


class Address(models.Model):

    EASTAZERBAIJAN = 'SA'
    WESTAZERBAIJAN  = 'WA'
    ARDABIL = 'AR'
    ESFAHAN = 'ES'
    ALBORZ = 'AL'
    EILAM = 'EI'
    BUSHEHR = 'BU'
    TEHRAN = 'TE'
    CHAHARMAHALVABAKHTIARI = 'CB'
    SOUTHKHORASAN = 'SK'
    KHORASANRAZAVI = 'KR'
    NORTHKHORASAN = 'NK'
    KHUZESTAN = 'KH'
    ZANJAN = 'ZA'
    SEMNAN = 'SE'
    SISTANVABALUCHESTAN = 'SB'
    FARS = 'FA'
    QAZVIN = 'QA'
    QOM = 'QO'
    KURDISTAN = 'KU'
    KERMAN = 'KE'
    KERMANSHAhH = 'KS'
    KOHGILOYEHVABOYERAHMAD = 'KB'
    GOLESTAN = 'GO'
    GILAN = 'GI'
    LORESTAN = 'LO'
    MAZANDARAN = 'MA'
    MARKAZI = 'MR'
    HORMOZGAN = 'HO'
    HAMEDAN = 'HA'
    YAZD = 'YA' 

    CITY_TYPE= (
            (EASTAZERBAIJAN, 'آذربایجان شرقی'),
            (WESTAZERBAIJAN, 'آذربایجان غربی'),
            (ARDABIL, 'اردبیل'),
            (ESFAHAN, 'اصفهان'),
            (ALBORZ, 'البرز'),
            (EILAM, 'ایلام'),
            (BUSHEHR, 'بوشهر'),
            (TEHRAN, 'تهران'),
            (CHAHARMAHALVABAKHTIARI, 'چهارمحال و بختیاری'),
            (SOUTHKHORASAN, 'خراسان جنوبی'),
            (KHORASANRAZAVI, 'خراسان رضوی'),
            (NORTHKHORASAN, 'خراسان شمالی'),
            (KHUZESTAN, 'خوزستان'),
            (ZANJAN, 'زنجان'),
            (SEMNAN, 'سمنان'),
            (SISTANVABALUCHESTAN, 'سیستان و بلوچستان'),
            (FARS, 'فارس'),
            (QAZVIN, 'قزوین'),
            (QOM, 'قم'),
            (KURDISTAN, 'کردستان'),
            (KERMAN, 'کرمان'),
            (KERMANSHAhH, 'کرمانشاه'),
            (KOHGILOYEHVABOYERAHMAD, 'کهگیلویه و بویراحمد'),
            (GOLESTAN, 'گلستان'),
            (GILAN, 'گیلان'),
            (LORESTAN, 'لرستان'),
            (MAZANDARAN, 'مازندران'),
            (MARKAZI, 'مرکزی'),
            (HORMOZGAN, 'هرمزگان'),
            (HAMEDAN, 'همدان'),
            (YAZD, 'یزد'),       
    )

    slug = models.SlugField(max_length=70, blank=True, unique=True, verbose_name='اسلاگ')
    label = models.CharField(max_length=50, unique=True, verbose_name='برچسب')
    city = models.CharField(choices=CITY_TYPE, max_length=2, verbose_name='شهر')
    address = models.TextField(help_text = gettext_lazy('بدون در نظر گرفتن نام شهر') ,verbose_name='آدرس')
    zipcode = models.CharField(max_length=11, verbose_name='کد پستی')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="user_address", verbose_name='کاربر')

    def random_number_generator(self):
        return '_' + str(random.randint(1000, 9999))

    def save(self, *args, **kwargs):
        self.label =  f'{self.label} {self.user.username}'
        self.address = f'{self.city} {self.address}'
        if not self.slug:
            self.slug = slugify(self.label) + '_address'
            while Address.objects.filter(slug = self.slug):
                self.slug = slugify(self.label)
                self.slug += self.random_number_generator()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.label} کاربر {self.user.id} با برچسب آدرس'
