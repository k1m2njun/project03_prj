import django_filters
from .models import RecipeList

class ListingFilter(django_filters.FilterSet):
    class Meta:
        model = RecipeList
        fields = {'rc_diff':['exact'],
                  'rc_time':['exact']}