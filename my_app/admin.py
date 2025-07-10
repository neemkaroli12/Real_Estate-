from django.contrib import admin
from .models import PropertySearch,Purpose,PropertyType,City,Location,newProject

# Register your models here.
admin.site.register(PropertySearch)
admin.site.register(Purpose)
admin.site.register(PropertyType)
admin.site.register(City)
admin.site.register(Location)


admin.site.register(newProject)

