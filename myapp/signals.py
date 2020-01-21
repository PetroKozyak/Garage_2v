from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import UserProfile


@receiver(post_save, sender=User, dispatch_uid="save_new_user_profile")
def save_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile(user=instance, first_name=instance.first_name, last_name=instance.last_name)
        profile.save()
