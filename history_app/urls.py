from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_history/', views.get_history, name='get_history'),
]