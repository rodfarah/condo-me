# Generated by Django 5.0.4 on 2024-05-08 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condo', '0004_remove_apartment_reservations_alter_commonarea_image_and_more'),
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='apartments',
            field=models.ManyToManyField(blank=True, related_name='reservations', to='condo.apartment'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_time',
            field=models.TimeField(verbose_name='User will end to use the common area at:'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_time',
            field=models.TimeField(verbose_name='User will start to use the common area at:'),
        ),
    ]
