from django.contrib import admin
from .models import Purpose, PropertyType, City, Location, newProject, Property, PropertyImage, LeadRequest, Lease, LeaseImage, Contact


# Basic model registrations
admin.site.register(Purpose)
admin.site.register(PropertyType)
admin.site.register(City)
admin.site.register(Location)
admin.site.register(newProject)
admin.site.register(PropertyImage)
admin.site.register(LeaseImage)
admin.site.register(Contact)

@admin.register(LeadRequest)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'whatsapp', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
    search_fields = ('name', 'whatsapp', 'property__location__name')

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('property_type', 'location', 'owner_user', 'owner_name', 'is_approved')
    list_filter = ('is_approved', 'owner_name', 'property_type', 'city')
    search_fields = ('owner_user__username', 'location__name', 'property_type__name', 'owner_name')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'property_type', 'location', 'city',
        'purpose', 'price', 'area', 'posted_by', 'is_approved'
    )
    list_filter = ('is_approved', 'city', 'property_type', 'purpose')
    search_fields = ('location__name', 'posted_by__username', 'property_type__name')
