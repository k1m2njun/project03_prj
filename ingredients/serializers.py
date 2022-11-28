from rest_framework import serializers
from .models import RecipeList

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeList
        fields = (
            'rc_diff',
            'rc_time'
        )