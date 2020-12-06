import uuid
import random
import json
from datetime import date
from requests.auth import HTTPBasicAuth

from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase


from exchanges.models import CurrencyExchage


class CurrencyExchageApiEmptyResposeTest(APITestCase):
    """ Test API empty response"""

    def test_empty_response(self):
        response = self.client.get(reverse('exchanges:api-exchange'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

class CurrencyExchageApiTest(APITestCase):
    """ Test API"""
    
    def setUp(self):
        CurrencyExchage.objects.insert(CurrencyExchage.BMX, 20.19, date.today())
        CurrencyExchage.objects.insert(CurrencyExchage.BANXICO, 19.98, date.today())
        CurrencyExchage.objects.insert(CurrencyExchage.FIXER, 19.95, date.today())

    def test_ok(self):
        response = self.client.get(reverse('exchanges:api-exchange'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

class CurrencyExchageApiThrottlingTest(APITestCase):
    """ Test API throttling"""
    
    def setUp(self):
        CurrencyExchage.objects.insert(CurrencyExchage.BMX, 20.19, date.today())
        CurrencyExchage.objects.insert(CurrencyExchage.BANXICO, 19.98, date.today())
        CurrencyExchage.objects.insert(CurrencyExchage.FIXER, 19.95, date.today())

    def test_throttling(self):
        """ throttling for anon user """
        max_req = int(settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['anon'].split('/')[0])
        for i in range(max_req+1):
            response = self.client.get(reverse('exchanges:api-exchange'))
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)