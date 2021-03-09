from django.urls import path

from . import views

urlpatterns = [
    path('', views.counter_view, name='counter'),
]