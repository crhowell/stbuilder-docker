from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.conf import settings

from profiles.models import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_handler(sender, instance, **kwargs):
    """As New User created, create and attach Profile"""
    if not kwargs.get('created'):
        return None
    profile = UserProfile(user=instance)
    profile.save()
