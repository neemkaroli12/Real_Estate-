
# class Slider(models.Model):
#     slide_img = models.ImageField(upload_to='slide_images/', null=True, blank=True)
    
#     def __str__(self):
#         return "Slide_Images"
    
from django.db import models

class Purpose(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class PropertyType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class PropertySearch(models.Model):
    purpose = models.ForeignKey(Purpose, on_delete=models.SET_NULL, null=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.purpose} - {self.property_type} in {self.city}"
    
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"{self.name} ({self.city.name})"
