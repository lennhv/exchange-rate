import logging
import datetime
from django_cron import CronJobBase, Schedule
from django.utils import timezone
from django.conf import settings

from .models import CurrencyExchage
from .clients import bmx_client, fixer_client, banxico_client

log = logging.getLogger(__name__)


def _str_to_date(s):
    try:
        return datetime.datetime.strptime(s, '%d/%m/%Y')
    except:
        return s


class BmxCronJob(CronJobBase):
    """ Cron job to syncs BMX USD to MXN exchange rate
    """
    RETRY_AFTER_FAILURE_MINS = 5
    RUN_AT_TIMES = ['06:00', '07:00', '08:00', '09:00', '10:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'exchanges.bmx_cron_job'

    def do(self):
        data = bmx_client(settings.BMX_TOKEN, [settings.BMX_DOLLAR_SERIE,])
        log.debug("BmxCronJob data %s", data)
        if not data:
            log.info("Empty data from Bmx Endpoint")
            return
        #
        CurrencyExchage.objects.insert(
            CurrencyExchage.BMX,
            data['bmx']['series'][0]['datos'][0]['dato'],
            _str_to_date(data['bmx']['series'][0]['datos'][0]['fecha'])
        )


class BanxicoCronJob(CronJobBase):
    """ Cron job to syncs BMX USD to MXN exchange rate
    """
    RETRY_AFTER_FAILURE_MINS = 5
    RUN_AT_TIMES = ['06:00', '07:00', '08:00', '09:00', '10:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'exchanges.banxico_cron_job'

    def do(self):
        data = banxico_client()
        log.debug("BanxicoCronJob data %s", data)
        if not data:
            log.info("Empty data from Banxico Endpoint")
            return
        #
        CurrencyExchage.objects.insert(
            CurrencyExchage.BANXICO,
            data['rate'],
            _str_to_date(data['date'])
        )


class FixerCronJob(CronJobBase):
    """ Cron job to syncs FIXER API latest currency exchange
    """
    RETRY_AFTER_FAILURE_MINS = 5
    RUN_AT_TIMES = ['06:00', '07:00', '08:00', '09:00',
                    '10:00', '11:00', '12:00', '13:00', '14:00',
                    '15:00', '16:00', '17:00', '18:00', '19:00', '20:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'exchanges.fixer_cron_job'

    def do(self):
        data = fixer_client(settings.FIXER_TOKEN)
        log.debug("FixerCronJob data %s", data)
        if not data:
            log.info("Empty data from Fixer Endpoint")
            return
        if not data['success']:
            log.info("Invalid response from Fixer %s", str(data))
            return
        #
        CurrencyExchage.objects.insert(
            CurrencyExchage.FIXER,
            data['rates']['MXN'],
            data['date']
        )
