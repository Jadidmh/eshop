from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Address, User
from django.utils.html import format_html

# Register your models here.

class AddressInline(admin.TabularInline):

    model = Address
    exclude = ('slug',)
    extra = 1

class UserAdmin(UserAdmin):

    search_fields = ('phone', 'username', 'email')
    list_filter = ('is_client', 'is_seller')
    list_display = ('phone', 'email', 'username', 'is_register', 'is_seller', 'is_client', 'show_image', 'date_joined')
    date_hierarchy = ('date_joined')

    @admin.display(empty_value='-',description="show image")
    def show_image(self, obj):
        if (obj.image):
            return format_html(
                '<img src="{}" width=50 height=50/>', obj.image.url,   
            )
        return '-'
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('phone', 'email', 'username'), 'password1', 'password2')
        }),
    )
    fieldsets = (
        (None, {
            'fields': ('phone', 'password', 'username', 'email', 'is_register', 'is_client', 'is_seller')
        }),

        ('more options', {
            'classes': ('collapse',),
            'fields':  ('first_name', 'last_name', 'image'),
        }),
    )

    save_on_top =True
    inlines = [
        AddressInline,
    ]
    list_editable = ('is_client', 'is_seller', 'is_register')

admin.site.register(User, UserAdmin)


class AddressAdmin(admin.ModelAdmin):
    search_fields = ('city',)
    list_filter = ('city',)
    list_display = ('label', 'user',  'city', 'zipcode', 'show_image')

    @admin.display(empty_value='-',description="show image")
    def show_image(self, obj):
        if (obj.user.image):
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.user.image.url,   
            )
        return '-'

    fieldsets = (
        (None, {
            'fields': ('user', 'label',  'city', 'address', 'zipcode')
        }),

        ('more options', {
            'classes': ('collapse',),
            'fields':  ('slug',),
        }),
    )

    list_per_page = 5

admin.site.register(Address, AddressAdmin)
