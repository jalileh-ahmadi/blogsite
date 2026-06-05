from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import os

class CustomUser(AbstractUser):
    allow_group_invites = models.BooleanField(
        default=True,
        help_text="اگر غیر فعال باشد، دیگر کاربران نمی‌توانند شما را به گروهی اضافه کنند.",
        verbose_name= 'ایا بقیه میتوانند مرا به گروهی اضافه کنند؟'
    )
    bio = models.TextField(blank=True, null=True, verbose_name='بیو')
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default_profile.png' , blank=True, verbose_name='عکس پروفایل')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        try:
            this_user = CustomUser.objects.get(id=self.id)
            if this_user.profile_image != self.profile_image:
                if this_user.profile_image.name != 'profiles/default_profile.png':
                    this_user.profile_image.delete(save=False)
        except CustomUser.DoesNotExist:
            pass

        if not self.profile_image:
            self.profile_image = 'profiles/default_profile.png'

        super().save(*args, **kwargs)

User = settings.AUTH_USER_MODEL


