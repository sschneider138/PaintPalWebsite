# Generated by Django 4.1.5 on 2023-06-17 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]