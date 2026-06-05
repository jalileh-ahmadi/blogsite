from django.db import models
from accounts.models import User

class Group(models.Model):
    name = models.CharField(max_length=225)
    image = models.ImageField(upload_to='group_profile')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group')
    member = models.ManyToManyField(User, related_name='group_memberships')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        try:
            group = Group.objects.get(id=self.id)
            if self.image != group.image:
                group.image.delete(save=False)
        except Group.DoesNotExist:
            pass
        super().save(*args, **kwargs)
        if is_new:
            self.member.add(self.admin)

    def __str__(self):
        return self.name



