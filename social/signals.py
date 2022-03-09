from django.db.models.signals import post_save  # after user is created make profile
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Musician


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        instance.musician.save()
    except ObjectDoesNotExist:
        Musician.objects.create(user=instance)
        

