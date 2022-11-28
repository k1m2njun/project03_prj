from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.post_list, name='ingredients'),
    # path("upload_image/", views.upload_image, name='upload_image'),
    # path("upload_text/", views.upload_text, name='upload_text'),
    path("upload_text/", views.UploadText.as_view(), name='upload_text'),
    path('upload_image/',views.MnistImageCreate.as_view(), name='upload_image'),
    path('image_result/<int:pk>/',views.image_result),
    # path('recipe_list/',views.RecipeListView.as_view()),
    path('recipe_list/',views.recommend,name='recipe_list'),
    path('delete_all/', views.delete_all),
    # path('recipe/',views.recommend_all, name='recipe_list_all'),
    path('recipe/',views.recommend_all, name='recipe_list_all'),
]

