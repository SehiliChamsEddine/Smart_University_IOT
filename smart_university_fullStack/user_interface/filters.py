import django_filters

from data_collect.models import *
 

class OrderFilter(django_filters.FilterSet):
    class Meta :
        model= Tempurature
        fields='__all__'