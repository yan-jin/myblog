from django.db import models
from django.utils import timezone
from django.urls import reverse


class Pictures(models.Model):
    picture = models.ImageField(upload_to='')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    # blog information
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=20, default='yanjin', blank=True)
    text = models.TextField(default='Oh! There\'s no text......')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(default=timezone.now)
    github = models.URLField(default='https://github.com/yan-jin', blank=True)
    img = models.ManyToManyField(Pictures, blank=True)
    # project information in index
    name = models.CharField(max_length=200)
    desc = models.TextField(default='Oh! There\'s no description......')
    icon = models.ImageField(blank=True, upload_to='')

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('blogapp:blog', kwargs={'pk': self.pk})


class HoleComment(models.Model):
    pid = models.CharField(max_length=20)
    cid = models.CharField(max_length=20)
    text = models.TextField()
    time = models.DateTimeField()


class Hole(models.Model):
    pid = models.CharField(max_length=30)
    text = models.TextField()
    comments = models.ManyToManyField(HoleComment, blank=True)
    time = models.DateTimeField()
    likes = models.CharField(max_length=20)
    comments_num = models.CharField(max_length=20)
