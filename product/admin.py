from django.contrib import admin
from .models import Product, Category, Tag, Shop
from django.utils.html import format_html

# Register your models here.

class CagetoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)
    list_display_link = ('title',)

admin.site.register(Category, CagetoryAdmin)


class TagAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)
    list_display_link = ('title',)

admin.site.register(Tag, TagAdmin)

class ShopAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('type', 'is_confirmed', 'is_deleted')
    list_display = ('name', 'type', 'address', 'seller', 'is_confirmed', 'is_deleted')

    @admin.action(description='Select shops to confirmed')
    def publish_shop(modeladmin, request, queryset):
        queryset.update(is_confirmed=True)


    actions = [publish_shop]
    list_editable = ('is_confirmed', 'is_deleted')

    fieldsets = (
    (None, {
        'fields': ('name', 'type', 'address', 'seller', 'is_confirmed')
    }),

    ('more options', {
        'classes': ('collapse', ),
        'fields':  ('is_deleted', 'slug'),
    }),
)

admin.site.register(Shop, ShopAdmin)

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name', 'descrption')
    list_filter = ('category', 'shop', 'is_confirmed')
    list_display = ('name', 'price', 'stock', 'image_tag', 'shop', 'is_confirmed',)
    readonly_fields = ('image_tag',)
    date_hierarchy = ('created_at')
    
    fieldsets = (
        (None, {
            'fields': (('name', 'price'), 'description', 'image',('shop', 'category'), 'tag', ('stock', 'weight'), 'discount')
        }),

        ('more options', {
            'classes': ('collapse',),
            'fields':  ('is_active', 'is_confirmed', 'slug'),
        }),
    )

    save_on_top =True
    list_per_page = 10
    list_editable = ('is_confirmed',)

admin.site.register(Product, ProductAdmin)
