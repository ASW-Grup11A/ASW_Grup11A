# Generated by Django 3.0.4 on 2020-04-30 18:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('empo_news', '0002_contribution_num_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contribution',
            name='num_likes',
        ),
        migrations.AddField(
            model_name='contribution',
            name='user_likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='contribution',
            name='likes',
        ),
        migrations.AddField(
            model_name='contribution',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]