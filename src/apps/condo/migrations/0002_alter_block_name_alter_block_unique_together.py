# Generated by Django 5.1.5 on 2025-01-24 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("condo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="block",
            name="name",
            field=models.CharField(default="Main Block", max_length=120),
        ),
        migrations.AlterUniqueTogether(
            name="block",
            unique_together={("name", "condominium")},
        ),
    ]
