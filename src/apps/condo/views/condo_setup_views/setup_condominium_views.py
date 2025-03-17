from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from apps.condo.forms import CondoSetupForm
from apps.condo.models import Condominium

from .base import SetupProgressMixin, SetupViewsWithDecors


class SetupCondominiumView(SetupViewsWithDecors, UpdateView, SetupProgressMixin):
    """A view class for setting up and managing condominiums.
    This view handles both creation and editing of condominium objects. It provides
    form handling, context data for templates, and associates condominiums with users.
    The view implements the following key functionalities:
    - Displays and processes the condominium setup form
    - Makes form fields readonly when editing existing condominiums
    - Provides context data about the existence of related objects
    - Associates newly created condominiums with the current user
    - Updates setup progress tracking
    - Handles success messages
    Attributes:
        model: The Condominium model class
        template_name: Path to the template for rendering the view
        form_class: The form class used for condominium setup
        success_url: URL to redirect to after successful form submission
    Inherits from:
        SetupViewsWithDecors: Base class for setup-related views
        UpdateView: Django's generic view for updating objects
        SetupProgressMixin: Mixin for tracking setup progress
    """

    model = Condominium
    template_name = "condo/pages/setup_pages/condominium/condo_setup_condominium.html"
    form_class = CondoSetupForm
    success_url = reverse_lazy("condo:condo_setup_home")

    def get_object(self, queryset=None):
        """
        This function subscribes get_object method and gets the
        "user condominium" object
        """
        return self.request.user.condominium

    def get_form(self, form_class=None):
        """
        Customizes the form by making fields readonly if a condominium already exists.
        This prevents direct editing of fields unless through the 'Edit' buttons.
        """
        form = super().get_form(form_class)
        #  "self.object" is the instance of "get_object()", the current condominium itself
        if self.object:
            for field in form.fields.values():
                field.widget.attrs["readonly"] = True
        return form

    def get_context_data(self, **kwargs):
        """
        Adds additional context data to the template.
        The 'condo_exists' flag helps the template determine whether to show
        creation or editing interfaces.
        """
        context = super().get_context_data(**kwargs)
        # check if condominium exists
        condominium = self.object
        if not condominium:
            context.update(
                {
                    "condo_exists": False,
                    "condo_cover": None,
                    "block_exists": False,
                    "apartment_exists": False,
                    "common_area_exists": False,
                }
            )
        else:
            related_objects = (
                condominium.blocks.exists(),
                condominium.apartments.exists(),
                condominium.common_areas.exists(),
            )
            # template needs all context elements, not only "condo_exists"
            context.update(
                {
                    "condo_exists": bool(condominium),
                    "condo_cover": getattr(condominium, "cover", None),
                    "block_exists": related_objects[0],
                    "apartment_exists": related_objects[1],
                    "common_area_exists": related_objects[2],
                }
            )

        return context

    def form_valid(self, form):
        """
        Called when a valid form data has been POSTed.
        Associates the condominium with the current user, creates initial setup
        progress and saves everything.
        """
        # If there is not a condominium object in form (new condominium)
        it_is_new_condo = not self.object

        # Save form first.
        # form_valid() returns HttpResponseRedirect (post > redirect > get)
        success_redirect = super().form_valid(form)
        condominium_instance = form.instance

        if it_is_new_condo:
            # Associate user with new condominium
            self.request.user.condominium = condominium_instance
            self.request.user.save()

            # Add user as condo_person
            current_user = get_user_model()
            current_user.objects.filter(id=self.request.user.id).update(
                condominium=condominium_instance
            )
        message = (
            "Condominium has been created successfully"
            if it_is_new_condo
            else "Condominium has been edited successfully"
        )
        messages.success(self.request, message)
        self.update_setup_progress()
        return success_redirect
