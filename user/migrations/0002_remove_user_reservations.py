# Generated by Django 5.0.4 on 2024-05-08 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='reservations',
        ),
    ]
