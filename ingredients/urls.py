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
    path('recipe/',views.recommend_all, name='recipe_list_all'),
    path('user_recipe/<int:pk>/',views.RecipePostDetail.as_view()),
    path('user_recipe/<int:pk>/new_comment/',views.new_comment),
    path("user_recipe/delete_comment/<int:pk>/", views.delete_comment), 
    path('user_recipe/',views.RecipePostList.as_view()),
    path('user_recipe/category/<str:slug>/',views.category_page),
    path('tag/<str:slug>/',views.tag_page),
    path('user_recipe/create_post/',views.RecipePostCreate.as_view()),
    path('user_recipe/update_post/<int:pk>/',views.RecipePostUpdate.as_view()),
    path("user_recipe/update_comment/<int:pk>/", views.CommentUpdate.as_view()),
    path('use_all/', views.use_all),
    path('trash_all/', views.trash_all),
    path('mypage/', views.UseTrashIView),
]

