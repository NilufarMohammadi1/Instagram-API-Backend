import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _




class Users(AbstractUser):
    class UserStatus(models.TextChoices):
        ACTIVE = 'AC', _('Active')
        DEACTIVE = 'DA', _('Deactive')
        DELETED = 'DL', _('Deleted')

    class GenderStatus(models.TextChoices):
        Female = 'FE', _('Female')
        MALE = 'MA', _('Male')
        NOTSAY = 'NS', _('Not Say')

    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    website = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=150, blank=True)
    gender = models.CharField(max_length=2, choices=GenderStatus.choices, default=GenderStatus.NOTSAY)
    is_private = models.BooleanField(default=False)
    avatar = models.CharField(max_length=255, blank=True)
    birthday = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=UserStatus.choices, default=UserStatus.ACTIVE)
    # followers = models.ManyToManyField('self', related_name='followers', blank=True)

    # in ahmagh nemire nemidonam chera
    # mikhad bere bashgah :))

    # username = models.CharField(max_length=50, unique=True)
    # email = models.EmailField(max_length=100, unique=True)

    # inam ye modele dg ke to khode user handle mikonim
    # kudum bhtre
    # age record hamon ziad bashe are on yeki behtare
    # to kodomo dost dari ? :)))))))))))))))))))))))))) toooooooooooooooooooooooooooooooooooooooooo
    # manam toro khelyyy dost daraaaam azizam
    # muuuuuchhhh

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = "Users"

    def full_name(self):
        return f'{self.username} and {self.gender} has an email {self.email}'

    def __str__(self):
        return self.username


class Followings(models.Model):
    id = models.UUIDField(default=uuid.uuid4, blank=False, primary_key=True)
    user_base = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_base')
    user_dest = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_dest')
    pending = models.BooleanField(default=False)
    accept_date = models.DateTimeField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)

