from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from .managers import CurrencyExchageManager


class CurrencyExchage(models.Model):
    """ Currency exchange rate Model
        Only keeps the latest rate by source and only for MXN to USD

        To add another source, it is necessary to define it as another choice,
         as well as those already defined.
    """
    BMX = 1
    BANXICO = 2
    FIXER = 3

    # source options
    SOURCES = (
        (BMX, _('BOLSA MEXICANA')),
        (BANXICO, _('BANXICO')),
        (FIXER, _('FIXER')),
    )

    source = models.SmallIntegerField(_('source'), choices=SOURCES)
    rate = models.FloatField(_('rate'),)
    date = models.DateField(_('date'),)
    last_update = models.DateTimeField(_('last_update'),)

    objects = CurrencyExchageManager()

    class Meta:
        verbose_name = _('currency exchange')
        verbose_name_plural = _('currencies exchange')

    def __str__(self):
        return "%s %s" % (self.source, self.rate)
