from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path("upload_text/", views.upload_text),
]
