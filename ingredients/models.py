from django.db import models

class Post(models.Model):
    ingredient = models.CharField(max_length=20)
    expiration_date = models.DateField(blank=True, null = True)    # 유통기한

    def __str__(self):
        return f'[{self.pk}] {self.ingredient}'
    