from django import forms 
from .models import Ingredients

class TextForm(forms.ModelForm):
    class Meta:
        model=Ingredients
        fields=['ingredient','expiration_date']
        labels = {
            'ingredient': '재료명',
            'expiration_date': '유통기한',
        }  
        
class RecipeListFilterForm(forms.Form):
    name = forms.CharField()