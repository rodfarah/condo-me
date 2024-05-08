# Generated by Django 5.0.4 on 2024-05-08 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_reservation_apartments_alter_reservation_end_time_and_more'),
        ('user', '0002_remove_user_reservations'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='users',
            field=models.ManyToManyField(related_name='reservations', to='user.user'),
        ),
    ]
