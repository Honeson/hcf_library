from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
import os
from django.utils import timezone
from django.template.defaultfilters import default, slugify



choices = (
    ('d', 'draft'),
    ('p', 'publish')
)


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'categories'

    
    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    path = f'posts/{instance.id}/{filename}'
    return path
def user_img_directory_path(instance, imgname):
    path = f'images/{instance.id}/{imgname}'
    return path

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique_for_date='published_date')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='library_posts', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    desc = models.CharField(max_length=1000)
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    status = models.CharField(max_length=1, choices=choices, default='p')
    published_date = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.slug])

    def publisher_get_absolute_url(self):
        return reverse('publisher_detail', args=[self.slug])

    class Meta:
        ordering = ('-published_date',)


class Chat(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    posted_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.message)


class FeedBack(models.Model):
    feedback = models.CharField(max_length=500, null=True, blank=True) 

    def __str(self):
        return self.feedback
