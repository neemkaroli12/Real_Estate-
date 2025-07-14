from django.db import models



class Purpose(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

class PropertyType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

class City(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='locations')
    def __str__(self): return f"{self.name} ({self.city.name})"

class Property(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="property/images", null=True, blank=True)
    purpose = models.ForeignKey(Purpose, on_delete=models.SET_NULL, null=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=1000)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.title} - {self.city.name}"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.title}"
    
    
#  7. New Project Section (For New/Upcoming Projects)
class newProject(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="newProject/images")
    summary = models.TextField(max_length=200, null=True, blank=True)
    pdf = models.FileField(upload_to="newProject/pdfs", null=True, blank=True)

    def __str__(self):
        return str(self.title) if self.title else "Unnamed Project"