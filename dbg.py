import os
import django
import sys

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehospitality.settings')
    django.setup()
    from django.db import connection
    print(f"Connected to: {connection.vendor}")
    from accounts.models import User
    print(f"User is_approved column exists: {'is_approved' in [f.name for f in User._meta.get_fields()]}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
