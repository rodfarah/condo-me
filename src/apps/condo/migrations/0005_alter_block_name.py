# Generated by Django 5.1 on 2025-01-03 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("condo", "0004_remove_block_unique_block_name_per_condo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="block",
            name="name",
            field=models.CharField(default="Main Block", max_length=120, unique=True),
        ),
    ]
