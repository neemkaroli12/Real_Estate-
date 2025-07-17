# my_app/utils.py
import requests
import random
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(phone_number, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        'authorization': settings.FAST2SMS_API_KEY,
        'sender_id': 'FSTSMS',
        'message': f'Your OTP is {otp}',
        'language': 'english',
        'route': 'otp',
        'numbers': phone_number,
    }
    headers = {
        'cache-control': "no-cache"
    }
    response = requests.post(url, data=payload, headers=headers)
    print("OTP Sent Response:", response.text)
    return response.status_code == 200
