from django.urls import path

from .api import CurrencyExchangeAPI


app_name = 'exchanges'

urlpatterns = [
    path('exchange/', CurrencyExchangeAPI.as_view(), name='api-exchange'),
]
