from django import forms 
from .models import Post

class TextForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['ingredient','expiration_date']
        labels = {
            'ingredient': '재료명',
            'expiration_date': '유통기한',
        }  