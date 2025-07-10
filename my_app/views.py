from django.shortcuts import render,get_object_or_404
from .forms import PropertySearchForm
from .models import PropertySearch,  City, newProject

def home(request):
    form = PropertySearchForm(request.GET or None)
    projects = newProject.objects.all() 
    results = None

    if form.is_valid():
        purpose = form.cleaned_data.get('purpose')
        property_type = form.cleaned_data.get('property_type')
        city = form.cleaned_data.get('city')

        results = PropertySearch.objects.filter(
            purpose=purpose,
            property_type=property_type,
            city=city,
            projects=projects,
        )
        return render(request, 'output.html', {"result": results})

    return render(request, 'index.html', {
        "form": form,
        "projects": projects  # <-- Yeh zaroori hai
    })



def city_detail(request, city_id):
    city = get_object_or_404(City, id=city_id)
    locations = city.locations.all()  # All locations of this city
    return render(request, 'city_detail.html', {
        'city': city,
        'locations': locations
    })
    
