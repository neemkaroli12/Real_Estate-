# from django.db import models

# from django.db import models

# class PurposeChoices(models.Model):
#     name = models.CharField(max_length=200, unique=True)
    
#     def __str__(self):
#         return self.name
    

# class PropertySearch(models.Model):
#     # PURPOSE_CHOICES = [
#     #     ('ps', 'Please Select'),
#     #     ('buy', 'Buy'),
#     #     ('rent', 'Rent'),
#     #     ('sell', 'Sell'),
#     #     ('lease', 'Lease'),
#     # ]

#     # PROPERTY_TYPE_CHOICES = [
#     #     ('ps', 'Please Select'),
#     #     ('apartment', 'Apartment'),
#     #     ('land', 'Land'),
#     #     ('cs', 'Commercial Space'),
        
#     # ]

#     # CITY_CHOICES = [
#     #     ('ps', 'Please Select'),
#     #     ('almora', 'Almora'),
#     #     ('bazpur', 'Bazpur'),
#     #     ('bageshwar', 'Bageshwar'),
#     #     ('berinag', 'Berinag'),
#     #     ('champawat', 'Champawat'),
#     #     ('chakrata', 'Chakrata'),
#     #     ('chamba', 'Chamba'),
#     #     ('dehradun', 'Dehradun'),
#     #     ('dharchula', 'Dharchula'),
#     #     ('gairsain', 'Gairsain'),
#     #     ('haridwar', 'Haridwar'),
#     #     ('jaspur', 'Jaspur'),
#     #     ('joshimath', 'Joshimath'),
#     #     ('kashipur', 'Kashipur'),
#     #     ('kichha', 'Kichha'),
#     #     ('kotdwar', 'Kotdwar'),
#     #     ('lohaghat', 'Lohaghat'),
#     #     ('manglaur', 'Manglaur'),
#     #     ('mussoorie', 'Mussoorie'),
#     #     ('nainital', 'Nainital'),
#     #     ('pauri', 'Pauri'),
#     #     ('pithoragarh', 'Pithoragarh'),
#     #     ('ramnagar', 'Ramnagar'),
#     #     ('rishikesh', 'Rishikesh'),
#     #     ('roorkee', 'Roorkee'),
#     #     ('rudraprayag', 'Rudraprayag'),
#     #     ('rudrapur', 'Rudrapur'),
#     #     ('srinagar', 'Srinagar'),
#     #     ('tanakpur', 'Tanakpur'),
#     #     ('tehri', 'Tehri'),
#     #     ('udhamsinghnagar', 'Udham Singh Nagar'),
#     #     ('uttarkashi', 'Uttarkashi'),
#     # ]

#     purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES, default='ps')
#     property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='ps')
#     city = models.CharField(max_length=30, choices=CITY_CHOICES, default='ps')

#     def __str__(self):
#         return f"{self.purpose} - {self.property_type} in {self.city}"

    
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

