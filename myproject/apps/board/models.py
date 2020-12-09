from django.db import models
from django.utils.html import mark_safe
from markdown import markdown

from django.contrib.auth.models import User


# 板块
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def last_post(self):
        post = Post.objects.filter(topic__board=self).order_by('-created_at').first()
        return post


# 主题
class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)  # <- here


# 帖子
class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    slug = models.SlugField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

# todo Tag
