# Generated by Django 5.0.4 on 2024-04-30 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='end_time',
            field=models.TimeField(verbose_name='Time user will end to use the common area'),
        ),
    ]