# Generated by Django 5.0.4 on 2024-07-22 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condo_people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to='condo_me/condominiums/%Y/%m/%d/'),
        ),
    ]
