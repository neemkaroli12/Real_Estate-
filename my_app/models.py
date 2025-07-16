from django.db import models
from django.contrib.auth.models import User


class Purpose(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PropertyType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Property(models.Model):
    title = models.CharField(max_length=200)
    purpose = models.ForeignKey(Purpose, on_delete=models.SET_NULL, null=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=1000)
    # Optional fields (add these only if you're using them in template)
    area = models.PositiveIntegerField(null=True, blank=True)
    length = models.PositiveIntegerField(null=True, blank=True)
    breadth = models.PositiveIntegerField(null=True, blank=True)
    open_sides = models.IntegerField(null=True, blank=True)
    facing = models.CharField(max_length=50, null=True, blank=True)
    construction_done = models.CharField(max_length=100, null=True, blank=True)
    boundary_wall = models.CharField(max_length=100, null=True, blank=True)
    ownership = models.CharField(max_length=100, null=True, blank=True)
    transaction_type = models.CharField(max_length=100, null=True, blank=True)
    overlooking = models.CharField(max_length=100, null=True, blank=True)

    agent_phone = models.CharField(max_length=15, null=True, blank=True)  # Contact no.
    brochure = models.FileField(upload_to='property/brochures/', null=True, blank=True)

    posted_on = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.city.name}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.title}"


class LeadRequest(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='leads')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"Lead for {self.property.title} by {self.name}"


class newProject(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="newProject/images")
    summary = models.TextField(max_length=200, null=True, blank=True)
    pdf = models.FileField(upload_to="newProject/pdfs", null=True, blank=True)

    def __str__(self):
        return self.title or "Unnamed Project"

