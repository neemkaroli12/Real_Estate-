from .models import City

def all_cities(request):
    return {'cities': City.objects.all()}