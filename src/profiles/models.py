import os
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


def get_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    return os.path.join('uploads/profiles/img', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to=get_upload_path, default='uploads/profiles/img/avatar.png', validators=[
        FileExtensionValidator(['png', 'jpg', 'jpeg'])
    ])
    website = models.CharField(max_length=220)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
