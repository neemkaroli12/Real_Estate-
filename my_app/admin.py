from django.contrib import admin
from .models import Purpose,PropertyType,City,Location,newProject,Property, PropertyImage,  LeadRequest,Lease,LeaseImage
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect

# Register your models here.

admin.site.register(Purpose)
admin.site.register(PropertyType)
admin.site.register(City)
admin.site.register(Location)
admin.site.register(newProject)
admin.site.register(PropertyImage)
admin.site.register(LeaseImage)
admin.site.register(Lease)
# admin.site.register(Sell)
# admin.site.register(SellImage)

@admin.register(LeadRequest)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'whatsapp', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
    
    
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [ 'posted_by', 'is_approved']
    list_filter = ['is_approved']
    actions = ['approve_properties']

    def approve_properties(self, request, queryset):
        queryset.update(is_approved=True)


class LeaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'location', 'price', 'owner_name', 'owner_user', 'is_approved')
    list_filter = ('city', 'is_approved')
    search_fields = ('owner_name', 'owner_user__username', 'location__name')

# @staff_member_required
# def approve_sell(request, sell_id):
#     sell = Sell.objects.get(id=sell_id)
#     sell.is_approved = True
#     sell.save()
#     return redirect('buy_properties')