from re import U
from django.urls import path
from . import views

urlpatterns = [
    path('about_me/', views.about_me),
    path('', views.landing),
    # path('signin/', views.signin, name='login'),    
    path('my_account/', views.my_account),
    path('signup/', views.signup),
    path('contact/', views.contact),
    path('event/', views.event),
    path('event/9/', views.ggimdak),
    
    ]
