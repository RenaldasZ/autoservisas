from django.urls import path
from . import views
from .views import car_list

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', car_list, name='car_list'),  
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
]