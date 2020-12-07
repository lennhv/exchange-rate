# exchange-rate
API to get latest USD to MXN exchange rate from different sources

Takes the exchange rate information from:

- Diario Oficial de la Federación
- Banxico
- Fixer.io

To avoid overload the sources with many requests it syncs the information every day using cron jobs.


# Deploy

- Download or clone this repo
- Create a .env file into the downloaded repo with the following data
```
SECRET_KEY={secrete key for django}
DEBUG={on or off}

DB_NAME={postgres database name}
DB_USER={postgres database user}
DB_PASSWORD={postgres database user password}

CACHE_URI={memcached connection uri}

BMX_TOKEN={Token for BMX API, see https://www.banxico.org.mx/SieAPIRest/service/v1/}
FIXER_TOKEN={token for fixer, see https://fixer.io/}
```
- Create virtual enviaron using:
```
pipenv install
```
- Activate venv
```
pipenv shell
```
-  Run migrations
```
python manage.py migrate
```
- Collect static files
```
python manage.py collectstatic
```
- Run test to ensure all works fine
```
python manage.py test
```
- Optionally create a super user
```
python manage.py createusperuser
```
- Run cronjobs to ensure that works fine
```
python manage.py runcrons
```
- Add command to cron, example
```
*/5 * * * * source /home/your-user/.bashrc && set -a && source /path/to/project/.env && set +a && source /path/to/project/.venv/bin/activate && python /path/to/project/exchangerate/manage.py runcrons
```
- Setup allowed host on settings.py
- Setup your wsgi server and nginx, i recomend uWSGI
- Go to your url 

# Live API

Go to http://hvz.io/exchangerate/doc/swagger/ 

It don't require authentication but is limited to 6 request/minute