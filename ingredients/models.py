from django.db import models
from django.contrib.auth.models import User

class Ingredients(models.Model):
    ingredient = models.CharField(max_length=20)
    expiration_date = models.DateField(blank=True, null = True)    # 유통기한
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # head_image = models.ImageField(upload_to='ingredients/images/%Y/%m/%d/')
    
    def __str__(self):
        return f'[{self.pk}] {self.ingredient}'
    
    def get_absolute_url(self):
        return f'/ingredients/'

class MnistImage(models.Model):
    head_image = models.ImageField(upload_to='ingredients/images/%Y/%m/%d/')
    result = models.CharField(max_length=30,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    expiration_date = models.DateField(blank=True, null = True)

    def __str__(self):
        return f'[{self.id}] {self.result}'

    def get_absolute_url(self):
        return f'/ingredients/image_result/{self.pk}/'

class RecipeList(models.Model):
    class DiffChoices(models.TextChoices):
        아무나 = '아무나'
        초급 = '초급'
        중급 = '중급'
        고급 = '고급'
        신 = '신의경지'
    class TimeChoices(models.TextChoices):
        오분 = '5분이내'
        십분 = '10분이내'
        십오분 = '15분이내'
        삼십분 = '30분이내'
        한시간 = '60분이내'
        한시간반 = '90분이내'
        두시간 = '2시간이내'
        두시간이상 = '2시간이상'
        
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
    rc_diff = models.CharField(max_length=100, blank=True, null=True, choices=DiffChoices.choices)
    rc_time = models.CharField(max_length=100, blank=True, null=True, choices=TimeChoices.choices)
    # author = models.ForeignKey("Author", on_delete=models.CASCADE)

