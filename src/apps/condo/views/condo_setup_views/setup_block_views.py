from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.condo.forms import BlockSetupForm
from apps.condo.models import Block

from .base import SetupProgressMixin, SetupViewsWithDecors


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
