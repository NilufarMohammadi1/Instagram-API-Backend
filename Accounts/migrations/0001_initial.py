# Generated by Django 4.0.3 on 2022-04-11 20:32

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('website', models.CharField(blank=True, max_length=100)),
                ('bio', models.TextField(blank=True, max_length=150)),
                ('gender', models.CharField(choices=[('FE', 'Female'), ('MA', 'Male'), ('NS', 'Not Say')], default='NS', max_length=2)),
                ('is_private', models.BooleanField(default=False)),
                ('avatar', models.CharField(blank=True, max_length=255)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('AC', 'Active'), ('DA', 'Deactive'), ('DL', 'Deleted')], default='AC', max_length=2)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Followings',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('user_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_base', to=settings.AUTH_USER_MODEL)),
                ('user_dest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_dest', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
