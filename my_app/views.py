from django.shortcuts import render, get_object_or_404
from .models import Property, Purpose, City,newProject
from .forms import PropertySearchForm



def home(request):
    form = PropertySearchForm(request.GET or None)
    results = None
    projects = newProject.objects.all()  

    if form.is_valid():
        purpose = form.cleaned_data['purpose']
        property_type = form.cleaned_data['property_type']
        city = form.cleaned_data['city']

        # If user selects "Buy", internally fetch properties with purpose "Sell"
        if purpose.name.lower() == "buy":
            try:
                purpose = Purpose.objects.get(name__iexact="Sell")
            except Purpose.DoesNotExist:
                purpose = None

        results = Property.objects.filter(
            purpose=purpose,
            property_type=property_type,
            city=city
        )

        return render(request, 'output.html', {
            'result': results,
            
        })

    return render(request, 'index.html', {
        'form': form,
        'projects': projects  
    })



#  Optional: City Detail Page (agar tum city-specific locations dikhati ho)
def city_detail(request, city_id):
    city = get_object_or_404(City, id=city_id)
    locations = city.locations.all()  # City ke related locations
    return render(request, 'city_detail.html', {
        'city': city,
        'locations': locations
    })


def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'property_detail.html', {
        'property': property_obj
    })
    
def buy_properties(request):
    try:
        sell_purpose = Purpose.objects.get(name__iexact="Sell")
        properties = Property.objects.filter(purpose=sell_purpose)
    except Purpose.DoesNotExist:
        properties = Property.objects.none()

    return render(request, 'buy.html', {'properties': properties})


def rent_properties(request):
    try:
        rent_purpose = Purpose.objects.get(name__iexact="Rent")
        properties = Property.objects.filter(purpose=rent_purpose)
    except Purpose.DoesNotExist:
        properties = Property.objects.none()

    return render(request, 'rent.html', {'properties': properties})


def lease_properties(request):
    try:
        lease_purpose = Purpose.objects.get(name__iexact="Lease")
        properties = Property.objects.filter(purpose=lease_purpose)
    except Purpose.DoesNotExist:
        properties = Property.objects.none()

    return render(request, 'lease.html', {'properties': properties})
