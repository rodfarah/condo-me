from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Case, IntegerField, Value, When
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.condo.forms import (
    ApartmentMultipleSetupForm,
    ApartmentSetupForm,
    BlockSetupForm,
    CondoSetupForm,
)
from apps.condo.models import Apartment, Block, Condominium, SetupProgress


# Create a 'manager group required' decorator
def manager_group_required(view_func):
    """
    This decorator checks if user belongs to 'manager' group.
    Redirects to the login page if the user does not belong to this group
    """

    def check_group(user):
        if user.groups.filter(name="manager").exists():
            return True
        raise PermissionDenied("You do not have the required permissions")

    return user_passes_test(
        test_func=check_group,
        login_url="/condo_people/login",
        redirect_field_name="redirect_to",
    )(view_func)


# Create a class that applies login_required and manager_group_required decorators
class SetupViewsWithDecors(View):
    """
    Ensures that only logged-in users who belong to the 'manager' group can access
    setup views.
    """

    @method_decorator(
        login_required(
            redirect_field_name="redirect_to", login_url="/condo_people/login"
        )
    )
    @method_decorator(manager_group_required)
    def dispatch(self, request, *args, **kwargs):
        """
        The dispatch method is overridden to add the manager_group_required decorator,
        ensuring that the group check occurs before anything else in the view.
        """
        return super().dispatch(request, *args, **kwargs)


class SetupProgressMixin:
    """
    Mixin to easily access and update condominium setup progress in views
    """

    def get_setup_progress(self):
        if not hasattr(self.request.user, "condominium"):
            return None

        return SetupProgress.objects.get_or_create(
            condominium=self.request.user.condominium
        )[0]

    def update_setup_progress(self):
        setup_progress = self.get_setup_progress()
        if setup_progress is not None:
            setup_progress.update_status()


class SetupAreaView(SetupViewsWithDecors):
    """
    'Setup Area' View is associated with the main 'condominium setup page', where manager
    user may configure the condominium itself, blocks, apartments, common areas,
    caretakers and residents.
    """

    template_name = "condo/pages/setup_pages/setup_main/condo_setup_home.html"

    def get(self, request):
        condominium = getattr(request.user, "condominium", None)
        context = {}

        if not condominium:
            context.update(
                {
                    "condo_exists": False,
                    "condo_cover": None,
                    "block_exists": False,
                    "apartment_exists": False,
                    "common_area_exists": False,
                    "setup_percentage": 0,
                    "next_step": None,
                    "is_setup_complete": False,
                }
            )
        else:
            # first, we get or create the "SetupProgress" object
            setup_progress, true_or_false = SetupProgress.objects.get_or_create(
                condominium=request.user.condominium
            )
            setup_progress.update_status()
            # then we add context variables to be sent to template
            context.update(
                {
                    "condo_exists": True,
                    "condo_cover": (
                        condominium.cover.name if condominium.cover else None
                    ),  # condominium cover url
                    "block_exists": condominium.blocks.exists(),
                    "apartment_exists": condominium.apartments.exists(),
                    "common_area_exists": condominium.common_areas.exists(),
                    "setup_percentage": setup_progress.setup_percentage,
                    "next_step": setup_progress.next_step,
                    "is_setup_complete": setup_progress.setup_percentage == 100,
                }
            )
        return render(
            request,
            self.template_name,
            context=context,
        )


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


class SetupBlockListView(SetupViewsWithDecors, ListView):
    """
    A view for displaying a list of Block objects in a condominium setup context.
    This view extends SetupViewsWithDecors and Django's ListView to display blocks
    that belong to the current user's condominium. It supports different template
    rendering modes based on the template_purpose attribute.
    Attributes:
        model (Model): The Django model class (Block) this view will query
        http_method_names (list): Restricts the view to only handle GET requests
        template_purpose (str): Determines which template to use for rendering
        templates (dict): Maps purpose identifiers to template paths
    Methods:
        get_queryset: Filters blocks to only show those belonging to the user's condominium
        get_template_names: Selects the appropriate template based on template_purpose
    """

    model = Block
    http_method_names = ["get"]
    template_purpose = "default"
    templates = {
        "default": "condo/pages/setup_pages/block/condo_setup_blocks.html",
        "apartments": "condo/pages/setup_pages/apartment/condo_setup_blocks_to_apartments.html",
    }

    def get_queryset(self):
        return Block.objects.filter(condominium=self.request.user.condominium).order_by(
            "number_or_name"
        )

    def get_template_names(self):
        template = self.templates.get(self.template_purpose, self.templates["default"])
        return template


class SetupBlockCreateView(SetupViewsWithDecors, CreateView, SetupProgressMixin):
    """
    A view for creating a new block in a condominium setup process.
    This view handles both GET and POST requests for creating new blocks within a condominium.
    It ensures that the user has an associated condominium before allowing block creation and
    validates that block names are unique within the condominium.
    Attributes:
        http_method_names (list): Allowed HTTP methods ['get', 'post']
        context_object_name (str): Name used for the block object in templates
        pk_url_kwarg (str): URL parameter name for block ID
        form_class: Form class used for block creation
        success_url: URL to redirect after successful block creation
        template_name (str): Template used for rendering the view
    Methods:
        dispatch: Validates that user has a condominium before proceeding
        form_valid: Handles form submission, validates block name uniqueness,
                   associates block with condominium and updates setup progress
    Inherits from:
        SetupViewsWithDecors
        CreateView
        SetupProgressMixin
    """

    http_method_names = ["get", "post"]
    context_object_name = "current_block"
    pk_url_kwarg = "block_id"
    form_class = BlockSetupForm
    success_url = reverse_lazy("condo:condo_setup_block_list")
    template_name = "condo/pages/setup_pages/block/condo_setup_block_create.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.condominium:
            messages.error(
                request,
                "In order to create a block, you must create a condominium first.",
            )
            return redirect("condo:condo_setup_condominium")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # get form instance without saving it
        self.object = form.save(commit=False)

        # Check if block name already exists in condominium
        if (
            Block.objects.filter(
                condominium=self.request.user.condominium,
                number_or_name__iexact=self.object.number_or_name,
            )
            .exclude(pk=self.object.pk)
            .exists()
        ):
            form.add_error(
                "number_or_name",
                "Block number (or name) already exists in this condominium. Please, choose a different one.",
            )
            return self.form_invalid(form)

        # associate user's condominium with block been created
        self.object.condominium = self.request.user.condominium

        # save new block
        self.object.save()

        # update setup progress bar
        self.update_setup_progress()

        messages.success(self.request, "Block has been created successfully.")
        return HttpResponseRedirect(self.get_success_url())


class SetupBlockEditView(SetupViewsWithDecors, UpdateView, SetupProgressMixin):
    """
    Class responsible for editing an existing condominium block.
    This view inherits from SetupViewsWithDecors, UpdateView and SetupProgressMixin to handle
    block editing functionality while ensuring proper setup progress tracking and decorators.
    Attributes:
        http_method_names (list): Allowed HTTP methods ('get' and 'post')
        context_object_name (str): Name used for the block object in templates
        form_class: Form class used for block editing
        model: Database model for blocks
        pk_url_kwarg (str): URL parameter name for block ID
        success_url: URL to redirect after successful edit
        template_name (str): Template used for rendering the edit form
    Methods:
        dispatch: Validates if user has a condominium and if block exists before processing
        get_context_data: Adds block_id to template context
        form_valid: Validates and processes the form submission, checking for duplicate block names
    Raises:
        None directly, but may show error messages through Django's message framework
    Returns:
        HttpResponseRedirect: Redirects to block list on success
        Rendered template: Shows edit form with error messages if validation fails
    """

    http_method_names = ["get", "post"]
    context_object_name = "current_block"
    form_class = BlockSetupForm
    model = Block
    pk_url_kwarg = "block_id"
    success_url = reverse_lazy("condo:condo_setup_block_list")
    template_name = "condo/pages/setup_pages/block/condo_setup_block_edit.html"

    def dispatch(self, request, *args, **kwargs):
        if not Block.objects.filter(
            condominium=self.request.user.condominium, pk=self.kwargs.get("block_id")
        ).exists():
            messages.error(
                request,
                "The block you are trying to edit does not exist, or you do not have\
                      permissions to do so.",
            )
            return redirect(reverse("condo:condo_setup_block_list"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["block_id"] = self.kwargs.get("block_id")
        return context

    def form_valid(self, form):
        # get form instance without saving it
        self.object = form.save(commit=False)

        # verify if block number_or_name already exists in condominium
        if (
            Block.objects.filter(
                condominium=self.request.user.condominium,
                number_or_name__iexact=self.object.number_or_name,
            )
            .exclude(pk=self.object.pk)
            .exists()
        ):
            form.add_error(
                "number_or_name",
                "Block number (or name) already exists in this condominium. Please, choose a different one.",
            )
            return self.form_invalid(form)

        # save updated block
        self.object.save()

        # update setup progress bar
        self.update_setup_progress()

        messages.success(self.request, "Block has been updated successfully.")
        return HttpResponseRedirect(self.get_success_url())


class SetupBlockDeleteView(SetupViewsWithDecors, DeleteView, SetupProgressMixin):
    """
    Class-based view for deleting Block instances in the condo setup process.
    This view provides functionality to delete a Block instance while maintaining setup progress tracking.
    It displays a confirmation page before deletion and handles the deletion process with appropriate
    user feedback.
    Attributes:
        model (Block): Model class to be used for deletion
        template_name (str): Path to the template used for rendering the deletion confirmation page
        success_url (str): URL to redirect to after successful deletion
        pk_url_kwarg (str): URL parameter name for the block's primary key
    Inherits From:
        SetupViewsWithDecors: Provides setup-specific decorators
        DeleteView: Django's generic view for deletion operations
        SetupProgressMixin: Handles setup progress tracking
    Usage:
        This view should be accessed through a URL pattern that provides a block_id parameter.
        It will show a confirmation page and handle the block deletion upon form submission.
    """

    model = Block
    template_name = "condo/pages/setup_pages/block/condo_setup_block_delete.html"
    success_url = reverse_lazy("condo:condo_setup_block_list")
    pk_url_kwarg = "block_id"

    def get_context_data(self, **kwargs):
        """
        Extends context data with block-specific information.

        Args:
            **kwargs: Additional context parameters

        Returns:
            dict: Context dictionary containing:
                - block_id: UUID of the block
                - block_name: number_or_name of the block
                - All other context data from parent classes
        """
        context = super().get_context_data(**kwargs)
        block_id = self.kwargs.get("block_id")
        block = get_object_or_404(Block, pk=block_id)
        context["current_block"] = block
        return context

    def form_valid(self, form):
        """
        Handles the deletion of Block instance.

        Extends DeleteView's form_valid to add a success message
        before redirecting user to success_url.

        Args:
            form: The form instance that triggered the deletion

        Returns:
            HttpResponseRedirect: Redirects to success_url after deletion
        """
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Block has been successfully deleted.")
        return HttpResponseRedirect(success_url)


class SetupApartmentsByBlockListView(SetupViewsWithDecors, ListView):
    """
    List view for displaying and managing apartments within a specific block during condominium setup.
    This view allows users to manage apartments for a selected block in their condominium.
    It provides the list of existing apartments and context for creating new ones.
    Inherits from:
        SetupViewsWithDecors: Base class for setup views with decorators
        ListView: Django generic list view
    Attributes:
        model (Model): Apartment model
        http_method_names (list): Allowed HTTP methods (only GET)
        template_name (str): Path to template for rendering the view
        context_object_name (str): Name of the context variable to store apartments list
    Methods:
        dispatch(request, *args, **kwargs):
            Validates if the requested block exists and belongs to user's condominium.
            Returns: HTTP response (redirect or super dispatch)
        get_queryset():
            Filters apartments by condominium and block.
            Returns: QuerySet of Apartment objects
        get_context_data(**kwargs):
            Adds the current block object to context.
            Returns: Context dictionary with block and apartments data
    """

    model = Apartment
    http_method_names = ["get"]
    template_name = (
        "condo/pages/setup_pages/apartment/condo_setup_apartments_by_block.html"
    )
    context_object_name = "apartments_in_block"

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch method to validate block access before proceeding.
        This method checks if the requested block exists and belongs to the user's condominium.
        If validation fails, redirects user back to block setup page with error message.
        Args:
            request: The HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments. Must contain 'block_id'
        Returns:
            HttpResponseRedirect: Redirects to block setup page if validation fails
            super().dispatch: Proceeds with normal dispatch if validation passes
        Raises:
            None
        """

        block_id = kwargs.get("block_id")
        if not Block.objects.filter(
            condominium=request.user.condominium, pk=block_id
        ).exists():
            messages.error(
                self.request,
                "The requested block does not exist or does not belong to your condominium.",
            )
            return redirect(reverse("condo:condo_setup_blocks_to_apartments"))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        block_id = self.kwargs.get("block_id")
        # return apartments in order (lowest to higher)
        return (
            Apartment.objects.filter(
                condominium=self.request.user.condominium,
                # Apartment has "block" attribute. Django creates "block_id" automatically
                block_id=block_id,
            ).annotate(
                # 0 for numeric values, 1 for non numeric (group numbers first)
                is_numeric=Case(
                    When(number_or_name__regex=r"^\d+$", then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField(),
                ),
                # convert num to int, uses 0 when text
                numeric_val=Case(
                    When(
                        number_or_name__regex=r"^\d+$",
                        then=Cast("number_or_name", IntegerField()),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                ),
            )
            # group by type (numbers first, text after)
            .order_by(
                "is_numeric",
                # For numbers, num asc sort
                "numeric_val",
                # For text, uses alphabetic sort
                "number_or_name",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        block_id = self.kwargs.get("block_id")
        context["current_block"] = Block.objects.get(
            condominium=self.request.user.condominium, pk=block_id
        )
        return context


class SetupApartmentCreateView(SetupViewsWithDecors, CreateView):
    """
    A view for creating new apartments within a specific block during condo setup.
    This view handles the creation of individual apartments within a condominium block.
    It ensures that apartments can only be created in existing blocks and associates
    them with the correct condominium and block.
    Attributes:
        model (Model): The Apartment model class
        context_object_name (str): Name used to reference the apartment in templates
        form_class (Form): The form class used for apartment creation
        http_method_names (list): Allowed HTTP methods (GET and POST)
        pk_url_kwarg (str): URL parameter name for the apartment ID
        template_name (str): Path to the template for apartment creation
    Methods:
        dispatch: Validates block existence before proceeding with the request
        get_context_data: Adds the current block to the template context
        get_success_url: Returns the URL to redirect after successful creation
        get_form_kwargs: Provides condominium and block context to the form
        form_valid: Handles the apartment creation and sets required relationships
    """

    model = Apartment
    context_object_name = "current_apartment"
    form_class = ApartmentSetupForm
    http_method_names = ["get", "post"]
    pk_url_kwarg = "apartment_id"
    template_name = "condo/pages/setup_pages/apartment/condo_setup_apartments_create_one_by_one.html"

    def dispatch(self, request, *args, **kwargs):
        # first, let's check if condominium exists
        if not request.user.condominium:
            messages.error(
                request,
                "In order to create apartments, you must create a condominium first.",
            )
            return redirect(reverse("condo:condo_setup_condominium"))

        # now, let's check if block exists
        block_id = self.kwargs.get("block_id")
        block_queryset = Block.objects.filter(
            condominium=self.request.user.condominium, pk=block_id
        )
        if not block_queryset.exists():
            messages.error(
                request,
                "You are trying to create apartments in a block that does not exist",
            )
            return redirect(reverse("condo:condo_setup_blocks_to_apartments"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_block = Block.objects.get(
            condominium=self.request.user.condominium, pk=self.kwargs.get("block_id")
        )
        context["current_block"] = current_block
        return context

    def get_success_url(self) -> str:
        return reverse(
            "condo:condo_setup_apartment_list_by_block",
            kwargs={"block_id": self.kwargs.get("block_id")},
        )

    def get_form_kwargs(self) -> dict:
        form_kwargs = super().get_form_kwargs()
        form_kwargs["condominium"] = self.request.user.condominium
        form_kwargs["block"] = Block.objects.get(
            condominium=self.request.user.condominium, pk=self.kwargs.get("block_id")
        )
        return form_kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        block = get_object_or_404(
            Block,
            condominium=self.request.user.condominium,
            pk=self.kwargs.get("block_id"),
        )
        self.object.condominium = self.request.user.condominium
        self.object.block = block
        self.object.save()
        messages.success(self.request, "Apartment has been created successfully.")
        return HttpResponseRedirect(self.get_success_url())


class SetupApartmentMultipleCreateView(SetupViewsWithDecors):
    """
    View for setting up and creating multiple apartments at once within a block.
    This view handles the workflow for bulk creating apartments, including:
    1. Initial form for specifying floor ranges and apartments per floor
    2. Confirmation page before final creation
    3. Apartment number generation based on floor ranges
    4. Bulk creation of apartments in the database
    The view verifies prerequisites such as:
    - Existence of a condominium
    - Existence of the specified block
    - Prevention of duplicate apartment numbers
    Flow:
    - GET: Displays the initial form for apartment generation parameters
    - POST: Processes the form and either shows confirmation or creates apartments
    - Redirects to apartment list on successful creation
    URL parameters:
        block_id: ID of the block where apartments will be created
    Session data:
        apartments_to_create: List of apartment numbers generated for confirmation
    """

    form_template = (
        "condo/pages/setup_pages/apartment/condo_setup_apartments_create_multiple.html"
    )
    confirmation_template = "condo/pages/setup_pages/apartment/condo_setup_apartments_confirm_create_multiple.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch method for apartment creation view.
        This method performs the following validations before proceeding:
        1. Checks if the user has a condominium associated with their account
        2. Verifies if the specified block exists within the user's condominium
        Parameters:
            request (HttpRequest): The HTTP request
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments, expected to contain 'block_id'
        Returns:
            HttpResponse: Redirects to appropriate setup page if validations fail,
                         otherwise proceeds with the standard dispatch
        """

        # Verify if condominium exists
        if not request.user.condominium:
            messages.error(
                request,
                "In order to create apartments, you must create a condominium first.",
            )
            return redirect(reverse("condo:condo_setup_condominium"))

        # verify if block exists
        block_id = self.kwargs.get("block_id")
        if not Block.objects.filter(
            condominium=request.user.condominium, pk=block_id
        ).exists():
            messages.error(
                request,
                "You are trying to create apartments in a block that does not exist",
            )
            return redirect(reverse("condo:condo_setup_blocks_to_apartments"))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests for apartment setup form.
        Renders the apartment setup form template with an empty ApartmentMultipleSetupForm and the current block
        information fetched from the database based on the user's condominium and the block_id from URL parameters.
        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, should contain 'block_id'.
        Returns:
            HttpResponse: Rendered template with the form and current block context.
        """

        form = ApartmentMultipleSetupForm()
        context = {
            "form": form,
            "current_block": Block.objects.get(
                condominium=self.request.user.condominium,
                pk=self.kwargs.get("block_id"),
            ),
        }
        return render(request, self.form_template, context=context)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to the condo setup view.
        This method processes either an initial form submission or a confirmation
        step, depending on the contents of the request.POST data.
        Parameters:
            request (HttpRequest): The request object containing POST data
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        Returns:
            HttpResponse: Either redirects after bulk creation or renders the
                         initial form processing response
        """
        # verify if last confirmation step
        if "Confirm" in request.POST:
            return self._bulk_create(request)
        else:
            # process initial form
            return self._process_initial_form(request)

    def _process_initial_form(self, request):
        """
        Process the initial form submission for setting up multiple apartments.
        This method validates the form data from the request. If the form is not valid,
        it re-renders the form template with error messages. If valid, it generates
        apartment numbers based on the form data, stores them in the session, and
        renders a confirmation template.
        Parameters:
        ----------
        request : HttpRequest
            The HTTP request object containing the form data in POST.
        Returns:
        -------
        HttpResponse
            Rendered template with either form errors or confirmation page.
        """
        form = ApartmentMultipleSetupForm(request.POST)

        if not form.is_valid():
            # render again with errors
            return render(
                request,
                self.form_template,
                {
                    "form": form,
                    "current_block": Block.objects.get(
                        condominium=request.user.condominium,
                        pk=self.kwargs.get("block_id"),
                    ),
                },
            )

        # extract form cleaned data
        form_data = form.cleaned_data

        # apply logic to create multiple apartments
        apartments_to_create = self._generate_apt_numbers(form_data)

        # save created items in session in order to be used on confirmation step
        request.session["apartments_to_create"] = apartments_to_create

        # generate context to be sent to confirmation template
        context = {
            "current_block": Block.objects.get(
                condominium=self.request.user.condominium,
                pk=self.kwargs.get("block_id"),
            ),
            "total_created_apartments": str(len(apartments_to_create)),
        }
        return render(request, self.confirmation_template, context=context)

    def _generate_apt_numbers(self, form_data):
        """
        Generate apartment numbers based on floor and apartment configuration.
        The function creates apartment numbers using a convention where each apartment number
        is formed by concatenating the floor number with a sequential apartment number.
        For example, apartment 2 on floor 3 would be numbered 32.
        Args:
            form_data (dict): A dictionary containing the following keys:
                - first_floor (int): The starting floor number
                - last_floor (int): The ending floor number (inclusive)
                - apartments_per_floor (int): Number of apartments on each floor
        Returns:
            list: A list of strings representing apartment numbers
        """

        first_floor = form_data["first_floor"]
        last_floor = form_data["last_floor"]
        apartments_per_floor = form_data["apartments_per_floor"]

        apartments_to_create = []

        floors = list(range(first_floor, last_floor + 1))

        for floor in floors:
            for n in range(apartments_per_floor):
                apartments_to_create.append(str(floor * 10 + (n + 1)))
        return apartments_to_create

    def _bulk_create(self, request):
        """
        Bulk creates multiple Apartment objects using data stored in the session.
        This method extracts apartment data from the session, checks for potential duplicates,
        and creates multiple apartments in a single database operation if validation passes.
        Args:
            request: The HTTP request object containing session data with apartments to create
        Returns:
            HttpResponseRedirect: Redirects to either the apartment list view on success or
            back to the creation form on failure
        Process:
            1. Retrieves apartment names/numbers from session
            2. Checks for existing apartments with the same names in the same block
            3. If duplicates exist, cancels the operation and shows error message
            4. Otherwise, creates all apartments in bulk and redirects to list view
            5. Shows appropriate messages indicating success or failure
        """
        apartments_to_create = request.session.get("apartments_to_create")
        if apartments_to_create:
            # check if apartments_to_create already exists in db
            existing_apartments = [
                apartment.number_or_name
                for apartment in Apartment.objects.filter(
                    condominium=request.user.condominium,
                    block__id=self.kwargs.get("block_id"),
                )
            ]
            duplicated_apartments = []
            for apto in apartments_to_create:
                if apto in existing_apartments:
                    duplicated_apartments.append(apto)
            if duplicated_apartments:
                current_block = Block.objects.get(
                    condominium=request.user.condominium, pk=self.kwargs.get("block_id")
                )
                messages.error(
                    request,
                    f"The whole operation was canceled because the following apartments already exist in {current_block.number_or_name}: {', '.join(duplicated_apartments)}. Please, consider creating manually (one by one) the apartments of this floor.",
                )
                return redirect(
                    reverse(
                        "condo:condo_setup_apartment_multiple_create",
                        kwargs={"block_id": self.kwargs.get("block_id")},
                    )
                )

            # get block
            block = Block.objects.get(
                condominium=request.user.condominium,
                pk=self.kwargs.get("block_id"),
            )
            # prepare list of apartment objects to be bulk created
            apartment_objects = [
                Apartment(
                    condominium=request.user.condominium,
                    block=block,
                    number_or_name=num_or_name,
                )
                for num_or_name in apartments_to_create
            ]
            # bulk_create objects in a single SQL operation
            Apartment.objects.bulk_create(apartment_objects)

            # delete session
            del request.session["apartments_to_create"]

            messages.success(
                request,
                f"Apartments {', '.join(str(apt) for apt in apartments_to_create)} have been created successfully",
            )
            return redirect(
                "condo:condo_setup_apartment_list_by_block", block_id=block.id
            )

        messages.error(
            request, "Please, fill in the blanks in order to create multiple apartments"
        )
        return redirect(
            reverse(
                "condo:condo_setup_apartment_multiple_create",
                kwargs={"block_id": self.kwargs.get("block_id")},
            )
        )


class SetupApartmentEditView(SetupViewsWithDecors, UpdateView, SetupProgressMixin):
    """
    View for editing an apartment in the condo setup process.
    This class handles the update operations for an Apartment object, providing both
    GET requests for displaying the edit form and POST requests for processing form submissions.
    It ensures that only users with access to the condominium can edit its apartments.
    Attributes:
        http_method_names (list): Allowed HTTP methods (POST and GET)
        context_object_name (str): Name used for the apartment object in the template context
        form_class: Form class used for apartment editing
        model: The Apartment model that this view operates on
        pk_url_kwarg (str): URL parameter name for the apartment ID
        template_name (str): Path to the template for rendering the edit form
    Methods:
        dispatch: Validates user permissions and apartment existence before proceeding
        get_queryset: Filters apartments to those belonging to the user's condominium
        get_context_data: Adds the block_id to the context for template rendering
        get_success_url: Determines the redirect URL after successful form submission
        form_valid: Handles form validation including checking for duplicate apartment names
                    within the same block before saving
    """

    http_method_names = ["post", "get"]
    context_object_name = "current_apartment"
    form_class = ApartmentSetupForm
    model = Apartment
    pk_url_kwarg = "apartment_id"
    template_name = "condo/pages/setup_pages/apartment/condo_setup_apartments_edit.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch method to verify that the requested apartment exists and
        belongs to the user's condominium before proceeding with the view execution.
        If the apartment doesn't exist or doesn't belong to the user's condominium,
        an error message is shown and the user is redirected to the blocks-to-apartments setup page.
        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, including apartment_id.
        Returns:
            HttpResponse: Either a redirect response if validation fails or the result of the parent's dispatch method.
        """

        apartment_queryset = Apartment.objects.filter(
            condominium=request.user.condominium,
            pk=self.kwargs.get("apartment_id"),
        )

        if not apartment_queryset.exists():
            messages.error(
                request,
                "The apartment you are trying to edit does not exist\
                            or you do not have permissions to do so.",
            )
            return redirect(
                reverse(
                    "condo:condo_setup_blocks_to_apartments",
                )
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Retrieves apartments belonging to the user's condominium as a security measure.

        This method ensures that users can only access apartment data from their own condominium,
        implementing a security boundary that prevents unauthorized access to other condominiums' data.

            QuerySet: Filtered apartment objects belonging to the authenticated user's condominium.
        """

        return Apartment.objects.filter(
            condominium=self.request.user.condominium,
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["block_id"] = self.object.block.id
        return context

    def get_success_url(self) -> str:
        return reverse(
            "condo:condo_setup_apartment_list_by_block",
            kwargs={"block_id": self.object.block.id},
        )

    def form_valid(self, form):
        # get form without saving it
        self.object = form.save(commit=False)

        # verify if apartment number already exists in block
        if (
            Apartment.objects.filter(
                condominium=self.request.user.condominium,
                block=self.object.block,
                number_or_name__iexact=self.object.number_or_name,
            )
            .exclude(pk=self.object.pk)
            .exists()
        ):
            form.add_error(
                "number_or_name",
                "Apartment number (or name) already exists in this block. Please, choose a different one.",
            )
            return self.form_invalid(form)

        # save updated apartment
        self.object.save()

        messages.success(self.request, "Apartment has been updated successfully.")
        return HttpResponseRedirect(self.get_success_url())


class SetupApartmentDeleteView(SetupViewsWithDecors, DeleteView):
    """
    A view for deleting apartment entries in the condo setup process.
    This view handles the deletion of Apartment model instances and provides
    confirmation before deletion. It includes context data for the confirmation
    template and handles success messages and redirects.
    Inherits:
        SetupViewsWithDecors: Base class containing setup-related decorators
        DeleteView: Django's generic delete view
    Attributes:
        model (Apartment): The model class to be deleted
        template_name (str): Path to the confirmation template
        pk_url_kwarg (str): URL parameter name for the apartment ID
    Methods:
        get_context_data: Adds apartment-specific data to template context
        get_success_url: Determines the URL to redirect after successful deletion
        form_valid: Handles the deletion process and success message
    Returns:
        HttpResponseRedirect: Redirects to the apartment list view after deletion
    """

    model = Apartment
    template_name = (
        "condo/pages/setup_pages/apartment/condo_setup_apartments_confirm_deletion.html"
    )
    pk_url_kwarg = "apartment_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["apartment_id"] = self.object.id
        context["apartment_num_or_name"] = self.object.number_or_name
        context["apartment_block"] = self.object.block
        return context

    def get_success_url(self) -> str:
        return reverse(
            "condo:condo_setup_apartment_list_by_block",
            kwargs={"block_id": self.object.block.id},
        )

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(
            self.request,
            f"Apartment {self.object.number_or_name} has been successfully deleted from {self.object.block}.",
        )
        return HttpResponseRedirect(success_url)
