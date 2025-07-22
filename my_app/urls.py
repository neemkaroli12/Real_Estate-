
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name="index"),  
    path('projects/', views.newprojects, name="projects"),  
    path('city/<int:city_id>/', views.city_detail, name='city_detail'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('verify-otp/<int:pk>/', views.verify_otp_view, name='verify_otp'),
    path('buy/', views.buy_properties, name='buy_properties'),
    path('rent/', views.rent_properties, name="rent_properties"),
    path('lease/', views.lease_properties, name="lease_properties"),
    path('post/', views.post_lease, name='post_lease'),  
    path('ajax/load-locations/', views.load_locations, name='ajax_load_locations'),
    path('lease/edit/<int:pk>/', views.edit_lease, name='edit_lease'),
    path('lease/delete/<int:pk>/', views.delete_lease, name='delete_lease'),
    path('post-property/', views.post_property, name='post_property'),
    path('signup/', views.signup, name='signup'),
    path('user-login/', views.user_login, name='user-login'),
    path('user-logout/', views.user_logout, name='user-logout'),
    path('sell/', views.sell_property, name='sell_property'),
    # path('get-locations/<int:city_id>/', views.get_locations, name='get_locations'),
] 






