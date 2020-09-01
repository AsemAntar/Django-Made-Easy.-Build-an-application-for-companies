import os
import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from profiles.models import Profile
from reports.models import Report, ProblemReported


LIKES_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class PostManager(models.Manager):
    def get_public(self):
        return self.filter(problem_reported__public=True)


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    liked = models.ManyToManyField(Profile, related_name='liked', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def num_likes(self):
        return self.liked.all().count()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class ProblemPost(Post):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    problem_reported = models.ForeignKey(
        ProblemReported, on_delete=models.CASCADE)
    objects = PostManager()

    def __str__(self):
        return f"{self.problem_reported.description[:50]}"

    def get_absolute_url(self):
        return reverse("posts:pp-detail", kwargs={'pk1': self.pk, 'pk': self.problem_reported.id})

    class Meta:
        verbose_name = 'Problem Post'
        verbose_name_plural = 'Problem Posts'


def get_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = f"{uuid.uuid4}.{extension}"
    return os.path.join('uploads/posts/images', filename)


class GeneralPost(Post):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=360)
    img = models.ImageField(upload_to=get_upload_path, blank=True, validators=[
                            FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:gp-detail", kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'General Post'
        verbose_name_plural = 'General Posts'


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(
        max_length=10, choices=LIKES_CHOICES, default="Like")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post} was {self.value}d"


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(GeneralPost, on_delete=models.CASCADE)
    body = models.TextField(max_length=360)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        ordering = ('-created',)
