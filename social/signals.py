# after user is created make profile
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Musician

# from tutorial https://www.youtube.com/watch?v=FdVuKt_iuSI
# start around 27minutes


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    When a user creates profile, django will use this
    signalto create a musician profile for the user
    """
    try:
        instance.musician.save()
    except ObjectDoesNotExist:
        Musician.objects.create(user=instance)
