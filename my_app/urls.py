
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name="index"),  
    path('city/<int:city_id>/', views.city_detail, name='city_detail'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('verify-otp/<int:pk>/', views.verify_otp_view, name='verify_otp'),
    path('buy/', views.buy_properties, name='buy_properties'),
    path('rent/', views.rent_properties, name="rent_properties"),
    path('lease/', views.lease_properties, name="lease_properties"),

] 



