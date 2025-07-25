
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name="index"),  
    path('projects/', views.newProject, name="projects"),  
    path('city/<int:city_id>/', views.city_detail, name='city_detail'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('verify-otp/<int:pk>/', views.verify_otp_view, name='verify_otp'),
    path('buy/', views.buy_properties, name='buy_properties'),
    path('rent/', views.rent_properties, name="rent_properties"),
    path('lease/', views.lease_properties, name="lease_properties"),
    path('post/', views.post_lease, name='post_lease'), 
    path('ajax/load-locations/', views.load_locations, name='ajax_load_locations'),
    path('signup/', views.signup, name='signup'),
    path('user-login/', views.user_login, name='user-login'),
    path('user-logout/', views.user_logout, name='user-logout'),
    path('sell/', views.sell_property_view, name='sell_property'),
    path('about/', views.about, name='about'),
    path('services/', views.service, name='services'),
   
] 






