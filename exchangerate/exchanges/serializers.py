from rest_framework import serializers

from .models import CurrencyExchage


class CurrencyExchangeSerializer(serializers.ModelSerializer):
    """ Serializer for currency exchange model
    """
    source = serializers.CharField(source='get_source_display')

    class Meta:
        model = CurrencyExchage
        fields = ('source', 'rate', 'date', 'last_update', )
