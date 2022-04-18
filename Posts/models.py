import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from Accounts.models import Users


class Tag(models.Model):

    class Meta:
        db_table = "Hashtags"

    title = models.CharField(max_length=100, primary_key=True)
    use_count = models.IntegerField(default=1)


class Posts(models.Model):
    class CategoryStatus(models.TextChoices):
        POST1 = 'P1', _('Post1')
        POST2 = 'P2', _('Post2')
        POST3 = 'P3', _('Post3')

    class PostStatus(models.TextChoices):
        WAITING = 'WI', _('Waiting')
        ACCEPTED = 'AC', _('Accepted')
        DELETED = 'DL', _('Delete')

    class Meta:
        db_table = "Posts"

    id = models.UUIDField(default=uuid.uuid4, blank=False, primary_key=True)
    caption = models.TextField(blank=True)
    category = models.CharField(max_length=2, choices=CategoryStatus.choices, default=CategoryStatus.POST1)
    status = models.CharField(max_length=2, choices=PostStatus.choices, default=PostStatus.WAITING)
    hashtag = models.ManyToManyField(Tag, blank=True)
    post_owner = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='post_owner')
    post_mentions = models.ManyToManyField(Users, blank=True, related_name='post_mentions')



class Media(models.Model):
    class MediaType(models.TextChoices):
        KNOWN = 'KN', _('Known')
        VIDEO = 'VI', _('Video')
        IMAGE = 'IM', _('Image')
        SOUND = 'SO', _('Sound')

    class Meta:
        db_table = "Media"

    id = models.UUIDField(default=uuid.uuid4, blank=False, primary_key=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=2, choices=MediaType.choices, default=MediaType.IMAGE)
    media_url = models.CharField(max_length=255)
    media_server_path = models.CharField(max_length=255)
    media_file_name = models.CharField(max_length=255)
    media_file_extension = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
