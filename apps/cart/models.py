from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.aggregates import Sum
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    user = models.OneToOneField(
        verbose_name=_('User'), to='users.User', related_name='cart', on_delete=models.CASCADE
    )

    @property
    def get_price(self):
        return self.items.aggregate(total=Sum('cost'))['total']

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f"{self.user.username}'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(
        verbose_name=_('Cart'), to='cart.Cart', related_name='items', on_delete=models.CASCADE, blank=True, null=True
    )
    device_id = models.CharField(verbose_name=_('Device id'), max_length=64, blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('carcover', 'polik', 'nakidka')}
    )
    object_id = models.PositiveIntegerField(verbose_name=_('Object id'))
    product = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'), default=0)
    cost = models.DecimalField(verbose_name=_('Cost'), max_digits=24, decimal_places=2, default=0)
    car_model = models.ForeignKey(verbose_name=_('Car model'), to='store.CarModel', related_name='cart_items', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')

    # TODO: cost ni hisoblab qo'yadigan algoritm yozish kerak
    def __str__(self):
        return f"{self.quantity} {self.product.title}(s) for {self.car_model}"

# TODO: Coupon system
# TODO: Kupit v odin klikni to'g'irlash kerak,logikasini va modellarini tuzish kerak
# TODO: Dostavka uchun, narxi uchun, kuni uchun model qilish kerak
# TODO: Working hours uchun model
# TODO: User yaralganida cart yaratilishi kerak