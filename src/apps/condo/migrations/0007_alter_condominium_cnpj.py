# Generated by Django 5.1 on 2024-12-06 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("condo", "0006_alter_block_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="condominium",
            name="cnpj",
            field=models.CharField(max_length=18, unique=True),
        ),
    ]
