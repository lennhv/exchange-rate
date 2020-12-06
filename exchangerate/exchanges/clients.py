import logging
import datetime
import requests
import pandas as pd

from django.conf import settings


log = logging.getLogger(__name__)


def _api_client(url, headers={}):
    """ Generic api client

        returns dict with response (asume response is a JSON)
    """
    log.debug("Request URL: %s", url)
    response = requests.get(url, headers=headers)
    log.debug("Response code: %s", response.status_code)
    if response.status_code != 200:
        return {}
    try:
        return response.json()
    except ValueError as e:
        return {}


def bmx_client(token, series, start_date=False, end_date=False):
    """ Bolsa Mexicana API
        https://www.banxico.org.mx/SieAPIRest/service/swagger-ui.html

        params:
            token: api token
            series: list of series to consult
            start_date: start search date, if not provided takes `today`
            end_date: end search date, if not provided takes `today`

        returns data dict 
    """
    headers = {
        'Accept': 'application/json',
        'Bmx-Token':  token,
    }

    if not start_date:
        start_date = datetime.date.today()
    if not end_date:
        end_date = datetime.date.today()
    id_series = ','.join(series)

    url = settings.BMX_ENDPOINT + \
        f'/v1/series/{id_series}/datos/{start_date}/{end_date}'

    respose = _api_client(url, headers=headers)

    return respose


def fixer_client(api_key, from_currency='USD', to_currencies=['MXN']):
    """ Fixer API client
        https://fixer.io/documentation

        params:
            api_key: API KEY
            from_currency: base currency
            to_currencies: list of currencies to be compared with base currency

        returns data dict 
    """

    # API allows get many currencies in the same request
    to_currencies = ','.join(to_currencies)

    url = settings.FIXER_ENDPOINT + \
        f'?access_key={api_key}&base={from_currency}&symbols={to_currencies}'

    respose = _api_client(url)

    return respose


def banxico_client(start_date=False, end_date=False):
    """ Banxico client

        Dowload `xls` file with exchange rates for current date
        extract data an save into a dict

        returns data dict
    """

    if not start_date:
        start_date = datetime.date.today().strftime('%d/%m/%Y')
    if not end_date:
        end_date = datetime.date.today().strftime('%d/%m/%Y')
    url = settings.BANXICO_ENDPOINT

    post_data = {
        'idioma': 'sp',
        'salida': 'XLS',
        'fechaInicial': start_date,
        'fechaFinal': end_date,
    }

    response = requests.post(url, data=post_data)

    if response.status_code != 200:
        return {}

    sheet = pd.read_excel(response.content, header=6, skiprows=[7])
    if len(sheet['Fecha']) == 0:
        return {}

    return {
        'date': datetime.datetime.strptime(sheet['Fecha'][0], '%d/%m/%Y'),
        'rate': sheet['Para solventar\nobligaciones'][0],
    }
