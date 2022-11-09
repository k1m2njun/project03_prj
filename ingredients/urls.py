from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.post_list, name='ingredients'),
    path("upload_image/", views.upload_image, name='upload_image'),
    path("upload_text/", views.upload_text, name='upload_text' ),
    path("create/", views.create, name='create'),
]
