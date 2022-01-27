# Generated by Django 3.2.10 on 2022-01-26 23:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='ایمیل')),
                ('phone', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message="شماره تلفن باید در قالب '09010944090' وارد شود.", regex='^09\\d{9}$')], verbose_name='تلفن همراه')),
                ('username', models.CharField(error_messages={'unique': 'کاربری با آن نام کاربری از قبل وجود دارد.'}, help_text='هشدار نام کاربری باید بین 1 تا 150 حرف باشد و (فقط از حروف، اعداد و . / + / - / _ استفاده شود)', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='نام کاربری باید حداقل یک حرف داشته باشد و @ پذیرفته نمی شود', regex='^[\\w.+-]*[a-zA-Z][\\w.+-]*\\Z')], verbose_name='نام کاربری')),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_image/', verbose_name='عکس')),
                ('is_client', models.BooleanField(default=False, help_text='مشخص می کند که آیا کاربر می تواند به عنوان مشتری وارد سیستم شود یا خیر.', verbose_name='مشتری هست')),
                ('is_seller', models.BooleanField(default=False, help_text='مشخص می کند که آیا کاربر می تواند به عنوان فروشنده وارد سیستم شود یا خیر.', verbose_name='فروشنده هست')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('slug', models.SlugField(blank=True, max_length=70, unique=True, verbose_name='اسلاگ')),
                ('label', models.CharField(max_length=50, unique=True, verbose_name='برچسب')),
                ('city', models.CharField(choices=[('SA', 'آذربایجان شرقی'), ('WA', 'آذربایجان غربی'), ('AR', 'اردبیل'), ('ES', 'اصفهان'), ('AL', 'البرز'), ('EI', 'ایلام'), ('BU', 'بوشهر'), ('TE', 'تهران'), ('CB', 'چهارمحال و بختیاری'), ('SK', 'خراسان جنوبی'), ('KR', 'خراسان رضوی'), ('NK', 'خراسان شمالی'), ('KH', 'خوزستان'), ('ZA', 'زنجان'), ('SE', 'سمنان'), ('SB', 'سیستان و بلوچستان'), ('FA', 'فارس'), ('QA', 'قزوین'), ('QO', 'قم'), ('KU', 'کردستان'), ('KE', 'کرمان'), ('KS', 'کرمانشاه'), ('KB', 'کهگیلویه و بویراحمد'), ('GO', 'گلستان'), ('GI', 'گیلان'), ('LO', 'لرستان'), ('MA', 'مازندران'), ('MR', 'مرکزی'), ('HO', 'هرمزگان'), ('HA', 'همدان'), ('YA', 'یزد')], max_length=2, verbose_name='شهر')),
                ('address', models.TextField(help_text='بدون در نظر گرفتن نام شهر', verbose_name='آدرس')),
                ('zipcode', models.CharField(max_length=11, verbose_name='کد پستی')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_address', serialize=False, to='user.user', verbose_name='کاربر')),
            ],
        ),
    ]
