from django.db import models, router
from django.db.models.constraints import UniqueConstraint
from django.db.models.deletion import Collector
from product.models import Shop, Product
from django.core.validators import MinValueValidator
from user.models import User

# Create your models here.


class Order(models.Model):
    CHECKING = "CH"
    CONFIRMED = "CO"
    CANCELED = "CA"

    STATUS_CHOICES = (
        (CHECKING, "در حال بررسی"),
        (CONFIRMED, "تایید شده"),
        (CANCELED, "لغو شد"),
    )
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="برای فروشگاه")
    items = models.ManyToManyField(Product, through='OrderItem', verbose_name="محصول")
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="مشتری")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True, default=0, verbose_name="قیمت کل")
    total_quantity = models.IntegerField(blank=True, default=0, verbose_name="مقدار کل")
    discount = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True, default=0, verbose_name="تخفیف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ایجاد شده در")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="به روز شده در")
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=CHECKING, verbose_name="وضعیت")
    is_payment = models.BooleanField(default=False, verbose_name="پرداخت شده")

    class Meta:
        ordering = ['-created_at',]
    
    def shop_order_total_price(self, slug):
        self.shop_total_price = 0
        order_items = self.orderitem_set.filter(product__shop__slug=slug)
        for item in order_items:
            self.shop_total_price += item.total_item_price
        return self.shop_total_price
    
    def shop_order_total_quantity(self, slug):
        self.shop_total_quantity = 0
        order_items = self.orderitem_set.filter(product__shop__slug=slug)
        for item in order_items:
            self.shop_total_quantity += item.quantity
        return self.shop_total_quantity

    def __str__(self):
        return f'order #{self.id} by {self.client.phone}'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)], blank=True)
    discount = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True, default=0)
    quantity = models.PositiveIntegerField(default=1)
    total_item_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['product', 'order']

    def __str__(self):
        return self.product.name
    
    def save(self, *args, **kwargs):
        if self.discount < self.product.discount:
            self.discount = self.product.discount
        if not self.unit_price:
            self.unit_price = self.product.price
        self.pr = (self.product.price * self.discount)/100
        self.total_item_price = self.product.price - self.pr
        
        self.order.total_price += self.total_item_price
        self.order.total_quantity += self.quantity
        self.order.save()
        self.product.stock -= self.quantity
        self.product.save()
        return super().save(*args, **kwargs)


    def delete(self, using=None, keep_parents=False):
        self.order.total_price -= self.total_item_price
        self.order.total_quantity -= self.quantity
        self.order.save()

        self.product.stock += self.quantity
        self.product.save()

        using = using or router.db_for_write(self.__class__, instance=self)
        assert self.pk is not None, (
            "%s object can't be deleted because its %s attribute is set to None." %
            (self._meta.object_name, self._meta.pk.attname)
        )
        collector = Collector(using=using)
        collector.collect([self], keep_parents=keep_parents)
        return collector.delete()