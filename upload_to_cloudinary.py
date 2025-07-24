import os
import django
import cloudinary
import cloudinary.uploader

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")  # change this
django.setup()

from my_app.models import Lease, LeaseImage  # change to your actual app name

# Cloudinary config
cloudinary.config(
    cloud_name='deux3exva',
    api_key='193136172139283',
    api_secret='Y352TZUSKwf05ziUkUHTzZogVpE'
)

MEDIA_FOLDER = 'media/leases'
MEDIA_FOLDER = 'media/property_images'

# ✅ Change this ID to match an actual Lease in your DB
lease = Lease.objects.get(id=1)

for filename in os.listdir(MEDIA_FOLDER):
    file_path = os.path.join(MEDIA_FOLDER, filename)
    if os.path.isfile(file_path):
        print(f"Uploading {filename}...")
        result = cloudinary.uploader.upload(file_path)
        print("✅ Uploaded:", result['secure_url'])

        # Save to DB
        LeaseImage.objects.create(
            lease=lease,
            image=result['secure_url']
        )
