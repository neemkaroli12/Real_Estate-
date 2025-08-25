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
    search_fields = ('name', 'whatsapp', 'property_location_name')

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('property_type', 'city', 'location', 'price', 'agent_name', 'contact_number')
    list_filter = ('city', 'location')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'property_type', 'location', 'city',
        'purpose', 'price', 'area', 'posted_by', 'is_approved'
    )
    list_filter = ('is_approved', 'city', 'property_type', 'purpose')
    search_fields = ('location_name', 'posted_byusername', 'property_type_name')

@admin.register(newProject)
class NewProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'summary')

