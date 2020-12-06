import uuid
import random
import json
from datetime import date, datetime
from requests.auth import HTTPBasicAuth

from django.urls import reverse
from django.conf import settings
from django.test import TestCase
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase
from django_cron.models import CronJobLog

from exchanges.models import CurrencyExchage
from exchanges.clients import bmx_client, fixer_client, banxico_client


class CurrencyExchageApiEmptyResposeTest(APITestCase):
    """ Test API empty response"""

    def test_empty_response(self):
        response = self.client.get(reverse('exchanges:api-exchange'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class CurrencyExchageApiTest(APITestCase):
    """ Test API"""

    def setUp(self):
        CurrencyExchage.objects.insert(
            CurrencyExchage.BMX, 20.19, date.today())
        CurrencyExchage.objects.insert(
            CurrencyExchage.BANXICO, 19.98, date.today())
        CurrencyExchage.objects.insert(
            CurrencyExchage.FIXER, 19.95, date.today())

    def test_ok(self):
        response = self.client.get(reverse('exchanges:api-exchange'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


class CurrencyExchageApiThrottlingTest(APITestCase):
    """ Test API throttling"""

    def setUp(self):
        CurrencyExchage.objects.insert(
            CurrencyExchage.BMX, 20.19, date.today())
        CurrencyExchage.objects.insert(
            CurrencyExchage.BANXICO, 19.98, date.today())
        CurrencyExchage.objects.insert(
            CurrencyExchage.FIXER, 19.95, date.today())

    def test_throttling(self):
        """ throttling for anon user """
        max_req = int(
            settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['anon'].split('/')[0])
        for i in range(max_req+1):
            response = self.client.get(reverse('exchanges:api-exchange'))
        self.assertEqual(response.status_code,
                         status.HTTP_429_TOO_MANY_REQUESTS)


class ClientsTest(APITestCase):

    def test_bmx_client(self):
        data = bmx_client(
            settings.BMX_TOKEN,
            [settings.BMX_DOLLAR_SERIE, ],
            '20202-12-04', '20202-12-04')
        self.assertEqual(len(data['bmx']['series']), 1)

    def test_baxico_client(self):
        data = banxico_client(start_date='04/12/2020', end_date='04/12/2020')
        self.assertTrue('rate' in data)
        self.assertTrue('date' in data)

    def test_fixer_client(self):
        data = fixer_client(settings.FIXER_TOKEN)
        self.assertTrue(data['success'])
        self.assertTrue('MXN' in data['rates'])
        self.assertTrue('date' in data)
