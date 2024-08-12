from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from condo.models import Apartment, Block, CommonArea, Condominium
from reservation.models import Reservation

from .models import User


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if Group.objects.filter(name="manager").exists():
        return

    groups_permissions = {
        "manager": [
            ("add_apartment", Apartment),
            ("delete_apartment", Apartment),
            ("view_apartment", Apartment),
            ("change_apartment", Apartment),
            ("add_block", Block),
            ("delete_block", Block),
            ("view_block", Block),
            ("change_block", Block),
            ("add_commonarea", CommonArea),
            ("delete_commonarea", CommonArea),
            ("view_commonarea", CommonArea),
            ("change_commonarea", CommonArea),
            ("change_condominium", Condominium),
            ("view_condominium", Condominium),
            ("add_reservation", Reservation),
            ("delete_reservation", Reservation),
            ("view_reservation", Reservation),
            ("change_reservation", Reservation),
            ("view_user", User),
            ("view_group", Group),
        ],
        "caretaker": [
            ("view_apartment", Apartment),
            ("view_block", Block),
            ("view_commonarea", CommonArea),
            ("view_condominium", Condominium),
            ("add_reservation", Reservation),
            ("delete_reservation", Reservation),
            ("view_reservation", Reservation),
            ("change_reservation", Reservation),
            ("view_user", User),
            ("view_group", Group),
        ],
        "resident": [
            ("view_apartment", Apartment),
            ("view_block", Block),
            ("view_commonarea", CommonArea),
            ("view_condominium", Condominium),
            ("add_reservation", Reservation),
            ("delete_reservation", Reservation),
            ("view_reservation", Reservation),
            ("change_reservation", Reservation),
            ("view_user", User),
        ],
    }

    for group_name, permissions in groups_permissions.items():
        # get_or_create() returns a tuple: the name , was created (True or False)
        group, now_created = Group.objects.get_or_create(name=group_name)
        for codename, model in permissions:
            # gets content type from model
            content_type = ContentType.objects.get_for_model(model)

            # creates or get the permission
            permission, _ = Permission.objects.get_or_create(
                codename=codename, content_type=content_type
            )

            group.permissions.add(permission)
