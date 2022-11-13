from django.db import models

class Post(models.Model):
    ingredient = models.CharField(max_length=20)
    expiration_date = models.DateField(blank=True, null = True)    # 유통기한
    head_image = models.ImageField(upload_to='ingredients/images/%Y/%m/%d/',null = True,blank=True)

    def __str__(self):
        return f'[{self.pk}] {self.ingredient}'


class MnistImage(models.Model):
    head_image = models.ImageField(upload_to='ingredients/images/%Y/%m/%d/')
    result = models.CharField(max_length=30,blank=True)

    def __str__(self):
        return f'[{self.id}] {self.result}'

    def get_absolute_url(self):
        return f'/ingredients/image_result/{self.pk}/'