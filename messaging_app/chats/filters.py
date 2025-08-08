import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    date_range = django_filters.DateFromToRangeFilter(field_name='timestamp')

    class Meta:
        model = Message
        fields = ['user', 'date_range']
