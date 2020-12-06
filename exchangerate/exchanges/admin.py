from django.contrib import admin

# Register your models here.
from .models import CurrencyExchage


@admin.register(CurrencyExchage)
class CurrencyExchageManager(admin.ModelAdmin):
    list_display = ('source', 'rate', 'last_update', 'date',)
