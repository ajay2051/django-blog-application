from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from . models import Profile



#Create Profile for each new user this function has been created

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# For saving profile

@receiver(post_save, sender=User)
def save_profile(sender, instance,  **kwargs):
    instance.profile.save()