from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Group

@receiver(post_delete, sender=Group)
def delete_group_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)