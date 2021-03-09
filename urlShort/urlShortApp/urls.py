from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:shrt_url>/', views.urlApi, name='urlApi'),
    path('shrt/<str:long_url>/', views.shortenUrl, name='shortenUrl'),
]