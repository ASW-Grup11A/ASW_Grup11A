# Generated by Django 3.0.4 on 2020-04-16 11:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2000)),
                ('points', models.IntegerField(default=1)),
                ('publication_time', models.DateTimeField(verbose_name='publication date')),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('text', models.CharField(blank=True, max_length=2000, null=True)),
                ('comments', models.IntegerField(default=0)),
                ('liked', models.BooleanField(default=True)),
                ('show', models.BooleanField(default=True)),
                ('hidden', models.ManyToManyField(blank=True, related_name='hide', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contribution', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('karma', models.IntegerField(default=1)),
                ('about', models.CharField(max_length=2000)),
                ('showdead', models.BooleanField(default=False)),
                ('noprocrast', models.BooleanField(default=False)),
                ('maxvisit', models.IntegerField(default=1)),
                ('minaway', models.IntegerField(default=180)),
                ('delay', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('contribution_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='empo_news.Contribution')),
                ('contribution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contrib', to='empo_news.Contribution')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='empo_news.Comment')),
            ],
            bases=('empo_news.contribution',),
        ),
    ]
