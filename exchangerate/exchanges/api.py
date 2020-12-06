from rest_framework.generics import ListAPIView

from .serializers import CurrencyExchangeSerializer
from .models import CurrencyExchage


class CurrencyExchangeAPI(ListAPIView):
    """ API, only GET allowed
    """
    queryset = CurrencyExchage.objects.all()
    serializer_class = CurrencyExchangeSerializer
