from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if os.getenv("CREATE_SUPERUSER") == "True":
        User = get_user_model()
        if not User.objects.filter(username="Adminmeena").exists():
            User.objects.create_superuser(
                username="Adminmeena",
                email="admin@ehospital.com",
                password="Adminmeena"
            )
