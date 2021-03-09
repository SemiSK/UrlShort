from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shrt/', views.shortenUrl, name='shortenUrl'),
    path('<str:shrt_url>/', views.urlApi, name='urlApi'),
]