# Generated by Django 5.1 on 2024-09-19 19:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("condo", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="commonarea",
            old_name="image",
            new_name="cover",
        ),
        migrations.RenameField(
            model_name="condominium",
            old_name="street",
            new_name="address1",
        ),
        migrations.RenameField(
            model_name="condominium",
            old_name="image",
            new_name="cover",
        ),
        migrations.RemoveField(
            model_name="condominium",
            name="complement",
        ),
        migrations.RemoveField(
            model_name="condominium",
            name="neighborwood",
        ),
        migrations.RemoveField(
            model_name="condominium",
            name="number",
        ),
        migrations.AddField(
            model_name="condominium",
            name="address2",
            field=models.CharField(default="", max_length=150),
        ),
        migrations.AlterField(
            model_name="condominium",
            name="cnpj",
            field=models.CharField(
                max_length=18,
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="CNPJ number mask must be XX.XXX.XXX/XXXX-XX",
                        regex="^\\d{2}\\.\\d{3}\\.\\d{3}\\/\\d{4}-\\d{2}$",
                    )
                ],
            ),
        ),
    ]