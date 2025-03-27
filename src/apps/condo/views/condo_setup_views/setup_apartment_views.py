from django.contrib import messages
from django.db.models import Case, IntegerField, Value, When
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.condo.forms import ApartmentMultipleSetupForm, ApartmentSetupForm
from apps.condo.models import Apartment, Block

from .base import SetupProgressMixin, SetupViewsWithDecors


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
                "The apartment you are trying to edit does not exist "
                "or you do not have permissions to do so.",
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

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden dispatch method to check if the user has permission to access the apartment.
        This method verifies that:
        1. The apartment with the given ID exists in the user's condominium
        2. The user has appropriate permissions to access/modify it
        If the apartment does not exist or the user doesn't have permission, it shows
        an error message and continues with the standard dispatch behavior.
        Parameters:
            request (HttpRequest): The HTTP request object containing user information
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments, including 'apartment_id'
        Returns:
            HttpResponse: The result of the parent class's dispatch method
        """

        if not Apartment.objects.filter(
            condominium=request.user.condominium, pk=self.kwargs.get("apartment_id")
        ).exists():
            messages.error(
                request,
                "The apartment you're trying to delete either doesn't exist or you don't have permission to delete it.",
            )
        return super().dispatch(request, *args, **kwargs)

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
