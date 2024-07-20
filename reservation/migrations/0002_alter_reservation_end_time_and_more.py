# Generated by Django 5.0.4 on 2024-07-20 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='end_time',
            field=models.TimeField(blank=True, help_text='Leave blank if this is a whole day use common area', null=True, verbose_name='Until:'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_time',
            field=models.TimeField(blank=True, help_text='Leave blank if this is a whole day use common area', null=True, verbose_name='From:'),
        ),
    ]