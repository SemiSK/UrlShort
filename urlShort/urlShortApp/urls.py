from django.urls import path

from . import views

urlpatterns = [
    path('', views.shortenUrl, name='index'),
    path('profile/', views.userProfile, name='userProfile'),
    path('<str:shrt_url>/', views.urlApi, name='urlApi'),
]