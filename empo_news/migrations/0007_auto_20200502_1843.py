# Generated by Django 3.0.4 on 2020-05-02 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empo_news', '0006_userfields_api_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfields',
            name='api_key',
            field=models.CharField(max_length=50, null=True),
        ),
    ]