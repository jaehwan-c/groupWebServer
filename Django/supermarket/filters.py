import django_filters
from .models import *
from .views import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        exclude = ('id','description','qr_code','entry_date')

class InstanceFilter(django_filters.FilterSet):
    class Meta:
        model = ItemInstance
        exclude = ('instanceId','user', 'status')