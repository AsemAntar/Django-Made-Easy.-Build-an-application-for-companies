# Generated by Django 3.0.3 on 2020-07-09 15:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reports', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile')),
                ('liked', models.ManyToManyField(blank=True, related_name='liked', to='profiles.Profile')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='GeneralPost',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='posts.Post')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=360)),
                ('img', models.ImageField(blank=True, upload_to=posts.models.get_upload_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])])),
            ],
            options={
                'verbose_name': 'General Post',
                'verbose_name_plural': 'General Posts',
            },
            bases=('posts.post',),
        ),
        migrations.CreateModel(
            name='ProblemPost',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='posts.Post')),
                ('problem_reported', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.ProblemReported')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Report')),
            ],
            options={
                'verbose_name': 'Problem Post',
                'verbose_name_plural': 'Problem Posts',
            },
            bases=('posts.post',),
        ),
    ]
