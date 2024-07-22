# Generated by Django 5.0.4 on 2024-07-22 18:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('condo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Reservation Date')),
                ('start_time', models.TimeField(blank=True, help_text='Leave blank if this is a whole day use common area', null=True, verbose_name='From:')),
                ('end_time', models.TimeField(blank=True, help_text='Leave blank if this is a whole day use common area', null=True, verbose_name='Until:')),
                ('share_with_others', models.BooleanField(verbose_name='Main user may share common area with other users?')),
                ('active', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('common_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='condo.commonarea')),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='condo.condominium')),
                ('user', models.ManyToManyField(related_name='reservations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
