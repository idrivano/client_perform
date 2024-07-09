from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Role

@receiver(post_migrate)
def populate_data(sender, **kwargs):
    if sender.name == 'services':
        # Insérer automatiquement des roles
        Role.objects.get_or_create(status='admin')
        Role.objects.get_or_create(status='member')
        Role.objects.get_or_create(status='user')