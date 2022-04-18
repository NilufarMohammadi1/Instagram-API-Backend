from django.db import models
from Posts.models import Posts
from Accounts.models import Users
import uuid


class Comments(models.Model):
    id = models.UUIDField(default=uuid.uuid4, blank=False, primary_key=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Comments"