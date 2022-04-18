# Generated by Django 4.0.3 on 2022-04-11 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('title', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('use_count', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'Hashtags',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('caption', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('P1', 'Post1'), ('P2', 'Post2'), ('P3', 'Post3')], default='P1', max_length=2)),
                ('status', models.CharField(choices=[('WI', 'Waiting'), ('AC', 'Accepted'), ('DL', 'Delete')], default='WI', max_length=2)),
                ('hashtag', models.ManyToManyField(blank=True, to='Posts.tag')),
                ('post_mentions', models.ManyToManyField(blank=True, related_name='post_mentions', to=settings.AUTH_USER_MODEL)),
                ('post_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('media_type', models.CharField(choices=[('KN', 'Known'), ('VI', 'Video'), ('IM', 'Image'), ('SO', 'Sound')], default='IM', max_length=2)),
                ('media_url', models.CharField(max_length=255)),
                ('media_server_path', models.CharField(max_length=255)),
                ('media_file_name', models.CharField(max_length=255)),
                ('media_file_extension', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Posts.posts')),
            ],
            options={
                'db_table': 'Media',
            },
        ),
    ]
