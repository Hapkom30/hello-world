from django_filters import FilterSet, DateTimeFilter
from .models import Post
from django.forms import DateTimeInput
class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = Post
        fields = {'title' : ['icontains'],
                  'category': ['exact']
                  }