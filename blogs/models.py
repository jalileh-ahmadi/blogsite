from django.db import models
from accounts.models import User
from django.utils.text import slugify
from unidecode import unidecode
from django.urls import reverse_lazy, reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug= slugify(unidecode(self.title))
        try:
            post = Post.objects.get(id=self.id)
            if self.image != post.image:
                post.image.delete(save=False)
        except Post.DoesNotExist:
            pass
        super(Post, self).save(*args, **kwargs)
