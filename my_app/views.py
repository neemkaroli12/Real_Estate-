from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, Purpose, City, newProject, PropertyImage, LeadRequest
from .forms import PropertySearchForm, LeadRequestForm
from django.conf import settings
import requests
import random
from .utils import send_otp, generate_otp


# Home page with search and project list
def home(request):
    form = PropertySearchForm(request.GET or None)
    results = None
    projects = newProject.objects.all()

    if form.is_valid():
        purpose = form.cleaned_data['purpose']
        property_type = form.cleaned_data['property_type']
        city = form.cleaned_data['city']

        # Auto-map "Buy" to "Sell"
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


# View properties for Buy
def buy_properties(request):
    try:
        sell_purpose = Purpose.objects.get(name__iexact="Sell")
        properties = Property.objects.filter(purpose=sell_purpose)
    except Purpose.DoesNotExist:
        properties = Property.objects.none()
    return render(request, 'buy.html', {'properties': properties})


# View properties for Rent
def rent_properties(request):
    try:
        rent_purpose = Purpose.objects.get(name__iexact="Rent")
        properties = Property.objects.filter(purpose=rent_purpose)
    except Purpose.DoesNotExist:
        properties = Property.objects.none()
    return render(request, 'rent.html', {'properties': properties})


# View properties for Lease
def lease_properties(request):
    try:
        lease_purpose = Purpose.objects.get(name__iexact="Lease")
        properties = Property.objects.filter(purpose=lease_purpose)
    except Purpose.DoesNotExist:
        properties = Property.objects.none()
    return render(request, 'lease.html', {'properties': properties})


# City detail to show locations and grouped properties
def city_detail(request, city_id):
    city = get_object_or_404(City, id=city_id)
    locations = city.locations.all()

    location_properties = []
    for location in locations:
        properties = Property.objects.filter(location=location)
        if properties.exists():
            location_properties.append({
                'location': location,
                'properties': properties
            })

    return render(request, 'city_detail.html', {
        'city': city,
        'location_properties': location_properties
    })


# Property detail page with contact modal and lead form
def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    related_properties = Property.objects.filter(city=property_obj.city).exclude(pk=pk)[:3]
    lead_form = LeadRequestForm()

    if request.method == 'POST' and 'lead_form_submit' in request.POST:
        lead_form = LeadRequestForm(request.POST)
        if lead_form.is_valid():
            lead = lead_form.save(commit=False)
            lead.property = property_obj

            otp = generate_otp()
            lead.otp = otp
            lead.save()

            phone = '91' + lead.whatsapp  # Send OTP on entered WhatsApp number
            send_otp(phone, otp)

            request.session['lead_id'] = lead.id
            return redirect('verify_otp', pk=pk)

    return render(request, 'property_detail.html', {
        'property': property_obj,
        'lead_form': lead_form,
        'related_properties': related_properties
    })



# OTP verification view (mock OTP = 123456)
def verify_otp_view(request, pk):
    lead_id = request.session.get('lead_id')
    lead = get_object_or_404(LeadRequest, id=lead_id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == lead.otp:
            lead.is_verified = True
            lead.save()
            return render(request, 'otp_success.html', {
                'lead': lead,
                'property': lead.property
            })
        else:
            return render(request, 'verify_otp.html', {
                'property': lead.property,
                'error': 'Invalid OTP'
            })

    return render(request, 'verify_otp.html', {'property': lead.property})

def send_sms_otp(phone_number):
    otp = str(random.randint(100000, 999999))
    
    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        'variables_values': otp,
        'route': 'otp',
        'numbers': phone_number
    }

    headers = {
        'authorization': settings.FAST2SMS_API_KEY,
        'Content-Type': "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    
    # For debugging (optional)
    print("SMS response:", response.text)

    return otp