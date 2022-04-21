import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class ProductFilter(django_filters.FilterSet):
    # start_data = DateFilter(field_name="published", lookup_expr='gte')
    # start_data = DateFilter(field_name="published", lookup_expr='lte')
    product_name = CharFilter(field_name="product_name", lookup_expr='icontains')
    bottle_capacity = CharFilter(field_name="bottle_capacity", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('product_name', 'bottle_capacity',)
