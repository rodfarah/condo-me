# Generated by Django 5.1 on 2024-09-05 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("purchase", "0003_rename_email_createmanagertoken_customer_email_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="CreateManagerToken",
            new_name="RegistrationToken",
        ),
    ]
