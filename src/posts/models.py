import os
import uuid

from django.core.validators import FileExtensionValidator
from django.db import models


from profiles.models import Profile
from reports.models import Report, ProblemReported


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

    def __str__(self):
        return f"{self.problem_reported.description[:50]}"

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

    class Meta:
        verbose_name = 'General Post'
        verbose_name_plural = 'General Posts'
