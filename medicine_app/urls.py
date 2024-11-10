from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('add/', views.add_medicine, name='add_medicine'),
    path('live-feed/', views.live_feed, name='live_feed'),
    path('capture-medicine-image/', views.capture_medicine_image, name='capture_medicine_image'),
]