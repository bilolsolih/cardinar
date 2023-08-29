from django.utils.translation import gettext_lazy as _

DELIVERY_TYPES = (
    ('s', _('Self-picked')),
    ('d', _('Delivery'))
)
ORDER_STATUS = (
    ('d', _('Delivered')),
    ('p', _('Pending'))
)
PAYMENT_STATUS = (
    ('wp', _('Waiting for payment')),
    ('pd', _('Paid'))
)
