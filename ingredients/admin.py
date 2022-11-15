from django.contrib import admin
from .models import Post, MnistImage

admin.site.register(Post)

admin.site.register(MnistImage)