from django.db import models
from django.utils import timezone


class CurrencyExchageManager(models.Manager):
    """ Manage for CurrencyExchage Model
    """

    def insert(self, source, rate, date):
        """ insert or update instance, this is because
        we need to keep only one row by `source`
        """
        instance, insert = self.update_or_create(
            source=source,
            defaults=dict(
                rate=rate,
                date=date,
                last_update=timezone.now())
        )
        return instance
