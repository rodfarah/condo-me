# Generated by Django 5.1 on 2024-10-04 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("condo", "0002_rename_image_commonarea_cover_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="condominium",
            name="cnpj",
            field=models.CharField(max_length=18, null=True, unique=True),
        ),
    ]
