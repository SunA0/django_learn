# Generated by Django 2.0.7 on 2020-11-28 17:22
from __future__ import unicode_literals
from django.db import migrations
from django.utils.text import slugify


def slugify_title(apps, schema_editor):
    model_post = apps.get_model('board', 'Post')
    for post in model_post.objects.all():
        post.slug = slugify(post.title)
        post.save()


class Migration(migrations.Migration):
    dependencies = [
        ('board', '0003_post_slug'),
    ]

    operations = [
    ]

# new