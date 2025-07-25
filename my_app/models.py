from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Purpose (e.g., Sell, Rent)
class Purpose(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Property Type (e.g., Apartment, Villa, Commercial)
class PropertyType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# City
class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Locality or Neighborhood
class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"{self.name} ({self.city.name})"

# Property Listing
class Property(models.Model):
    purpose = models.ForeignKey(Purpose, on_delete=models.SET_NULL, null=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    area = models.PositiveIntegerField(null=True, blank=True)  # in sq.ft
    description = models.TextField(max_length=1000)
    facing = models.CharField(max_length=50, null=True, blank=True)
    ownership = models.CharField(max_length=100, null=True, blank=True)
    transaction_type = models.CharField(max_length=100, null=True, blank=True)
    agent_phone = models.CharField(max_length=15, null=True, blank=True)
    brochure = CloudinaryField(resource_type='raw', folder='property/brochures/') 
    posted_on = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property_type} in {self.location} by {self.posted_by}"

# Multiple images per property
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder='property/')
    def __str__(self):
       return f"Image for {self.property} #{self.property.id}"




# Inquiries / Lead Requests
class LeadRequest(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='leads')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead by {self.name} for {self.property.property_type} at {self.property.location}"

# Projects section
class newProject(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    image = CloudinaryField('image', folder='newprojects/')
    summary = models.TextField(max_length=500, null=True, blank=True)
    brochure = CloudinaryField(resource_type='raw', folder='newprojects/brochures/') 

    def __str__(self):
        return self.title or "Unnamed Project"

# Lease listing

class Lease(models.Model):
    owner_user = models.ForeignKey(User, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    area = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    owner_name = models.CharField(max_length=100, null=True)
    contact_name = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=15, null=True)
    description = models.TextField(null=True, blank=True)  
    terms_and_conditions = models.TextField(null=True, blank=True) 
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property_type} in {self.location} by {self.owner_user}"


class LeaseImage(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', folder='leases/')
    def __str__(self):
        return f"Image for #{self.lease.id}"