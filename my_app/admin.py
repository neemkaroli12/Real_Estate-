from django.contrib import admin
from .models import Purpose,PropertyType,City,Location,newProject,Property, PropertyImage

# Register your models here.
# admin.site.register(PropertySearch)
admin.site.register(Purpose)
admin.site.register(PropertyType)
admin.site.register(City)
admin.site.register(Location)
admin.site.register(newProject)
admin.site.register(PropertyImage)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'posted_by']

admin.site.register(Property, PropertyAdmin)


