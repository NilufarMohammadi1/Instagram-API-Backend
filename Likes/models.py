from django.db import models
from Posts.models import Posts
from Accounts.models import Users
import uuid


class Likes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, blank=False, primary_key=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Likes"