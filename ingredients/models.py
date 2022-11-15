from django.db import models
from django.contrib.auth.models import User

class Ingredients(models.Model):
    ingredient = models.CharField(max_length=20)
    expiration_date = models.DateField(blank=True, null = True)    # 유통기한
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # head_image = models.ImageField(upload_to='ingredients/images/%Y/%m/%d/')
    
    def __str__(self):
        return f'[{self.pk}] {self.ingredient}'

class MnistImage(models.Model):
    head_image = models.ImageField(upload_to='ingredients/images/%Y/%m/%d/')
    result = models.CharField(max_length=30,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.id}] {self.result}'

    def get_absolute_url(self):
        return f'/ingredients/image_result/{self.pk}/'

class RecipeList(models.Model):
    rc_num = models.IntegerField(blank=True, null=True)
    rc_name = models.CharField(max_length=100, blank=True, null=True)
    rc_view = models.IntegerField(blank=True, null=True)
    rc_rec = models.IntegerField(blank=True, null=True)
    rc_scrap = models.IntegerField(blank=True, null=True)
    rc_type = models.CharField(max_length=100, blank=True, null=True)
    rc_sit = models.CharField(max_length=100, blank=True, null=True)
    rc_sort = models.CharField(max_length=100, blank=True, null=True)
    rc_nick = models.CharField(max_length=100, blank=True, null=True)
    rc_info = models.CharField(max_length=100, blank=True, null=True)
    rc_ing = models.CharField(max_length=200, blank=True, null=True)
    rc_diff = models.CharField(max_length=100, blank=True, null=True)
    rc_time = models.CharField(max_length=100, blank=True, null=True)