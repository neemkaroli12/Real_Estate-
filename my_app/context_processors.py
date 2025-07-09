# myblog_app/context_processors.py

from .models import Location

def location_dropdown(request):
    locations = Location.objects.all()
    return {'locations': locations}
