from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_delete, sender=CustomUser)
def delete_account_image(sender, instance, **kwargs):
    if instance.profile_image.name != 'profiles/default_profile.png':
        instance.profile_image.delete(save=False)
