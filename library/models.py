from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
import os



choices = (
    ('d', 'draft'),
    ('p', 'publish')
)

def user_directory_path(instance, filename):
    path = f'posts/{instance.id}/{filename}'
    return path
def user_img_directory_path(instance, imgname):
    path = f'images/{instance.id}/{imgname}'
    return path

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='library_posts')
    desc = models.CharField(max_length=1000)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    status = models.CharField(max_length=1, choices=choices, default='p')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        self.img.delete()
        super().delete(*args, **kwargs)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension