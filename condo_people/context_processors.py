from django.contrib.auth.models import Group


def user_groups(request):
    """
    Using booleans, this function checks which group a user belongs;
    """
    if request.user.is_authenticated:
        is_manager = request.user.groups.filter(name="manager").exists()
        is_caretaker = request.user.groups.filter(name="caretaker").exists()
        is_resident = request.user.groups.filter(name="resident").exists()
    else:
        is_manager = False
        is_caretaker = False
        is_resident = False

    return {
        "is_manager": is_manager,
        "is_caretaker": is_caretaker,
        "is_resident": is_resident,
    }
