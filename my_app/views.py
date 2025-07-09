from django.shortcuts import render,get_object_or_404
from .forms import PropertySearchForm
from .models import PropertySearch

def home(request):
    form = PropertySearchForm(request.GET or None)
    results = None

    # Only filter if the form is submitted and valid
    if form.is_valid():
        purpose = form.cleaned_data.get('purpose')
        property_type = form.cleaned_data.get('property_type')
        city = form.cleaned_data.get('city')

        # Filter the PropertySearch model based on input
        results = PropertySearch.objects.filter(
            purpose=purpose,
            property_type=property_type,
            city=city
        )
        return render(request, 'output.html', {"result": results})#use new page here that will display the output after search
        

    form = PropertySearchForm()

    return render(request, 'index.html', {"form": form})

from .models import City

def city_detail(request, city_id):
    city = get_object_or_404(City, id=city_id)
    locations = city.locations.all()  # All locations of this city
    return render(request, 'city_detail.html', {
        'city': city,
        'locations': locations
    })