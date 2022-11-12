from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.post_list, name='ingredients'),
    # path("upload_image/", views.upload_image, name='upload_image'),
    path("upload_text/", views.upload_text, name='upload_text' ),
    path('create_image/',views.MnistImageCreate.as_view()),
    path('image_result/<int:pk>/',views.image_result),
]
