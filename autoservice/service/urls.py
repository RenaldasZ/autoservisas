from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.car_list, name='car_list'),  
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('myorders/', views.UserOrdersListView.as_view(), name='my_orders'),
    path('myorders/<int:pk>', views.UserOrderDetailView.as_view(), name='my_order'),
    path('myorders/new', views.UserOrderCreateView.as_view(), name='my-order-new'),
    path('mycars/', views.UserCarListView.as_view(), name='my_cars'),
    path('mycars/new', views.UserCarCreateView.as_view(), name='my-car-new'),
    path('car/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('order/<int:order_pk>/create-service/', views.OrderEntryCreateView.as_view(), name='create_service'),
]