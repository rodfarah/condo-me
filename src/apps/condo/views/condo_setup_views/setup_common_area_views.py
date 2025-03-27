from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.condo.forms import CommonAreaSetupForm
from apps.condo.models import CommonArea

from .base import SetupProgressMixin, SetupViewsWithDecors


class SetupCommonAreaListView(SetupViewsWithDecors, ListView):
    """
    A view that displays a list of common areas for a condominium setup.
    This view inherits from SetupViewsWithDecors and ListView to display all common areas
    associated with the current user's condominium. It handles only GET requests and renders
    the data using the specified template.
    Attributes:
        model (Model): The CommonArea model to use for the view.
        http_method_names (list): List of HTTP methods the view accepts. Only GET is allowed.
        template_name (str): Path to the template used to render the common area list.
        context_object_name (str): Name of the variable to use in the template context.
    Methods:
        get_queryset(): Returns a QuerySet of CommonArea objects filtered by the user's condominium.
    """

    model = CommonArea
    http_method_names = ["get"]
    template_name = (
        "condo/pages/setup_pages/common_area/condo_setup_common_area_list.html"
    )
    context_object_name = "common_area_list"

    def get_queryset(self):
        return CommonArea.objects.filter(
            condominium=self.request.user.condominium,
        )


class SetupCommonAreaCreateView(SetupViewsWithDecors, CreateView, SetupProgressMixin):
    """
    View for creating a common area in a condominium setup process.
    This view handles the creation of common areas within a condominium. It ensures
    that a condominium exists before allowing common area creation, validates that
    the common area name is unique within the condominium, and associates the newly
    created common area with the user's condominium.
    Attributes:
        http_method_names (list): Allowed HTTP methods (GET and POST)
        context_object_name (str): Name used for the current common area in templates
        form_class (Form): Form class for common area setup
        model (Model): Database model for common area
        pk_url_kwarg (str): URL keyword argument for primary key
        success_url (str): URL to redirect after successful creation
        template_name (str): Template used for rendering the view
    Methods:
        dispatch: Ensures a condominium exists before proceeding
        form_valid: Validates the form, checks for name uniqueness, associates
                    the common area with the user's condominium, and updates
                    the setup progress
    """

    http_method_names = ["get", "post"]
    context_object_name = "current_common_area"
    form_class = CommonAreaSetupForm
    model = CommonArea
    pk_url_kwarg = "common_area_id"
    success_url = reverse_lazy("condo:condo_setup_common_area_list")
    template_name = (
        "condo/pages/setup_pages/common_area/condo_setup_common_area_create.html"
    )

    def dispatch(self, request, *args, **kwargs):
        """
        Overrides the default dispatch method to ensure a user has a condominium associated before allowing access.
        If the user does not have a condominium, they are redirected to the condominium setup page
        with an error message. Otherwise, the request is processed normally.
        Args:
            request: The HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        Returns:
            HttpResponseRedirect: Redirects to condominium setup if user has no condominium
            Super result: Otherwise returns the result of the parent class's dispatch method
        """

        if not request.user.condominium:
            messages.error(
                request,
                "In order to create a common area, you must create a condominium first",
            )
            return redirect("condo:condo_setup_condominium")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # get form instance without saving it
        self.object = form.save(commit=False)

        # check if Common Area name already exists in condominium
        if (
            CommonArea.objects.filter(
                condominium=self.request.user.condominium, name__iexact=self.object.name
            )
            .exclude(pk=self.object.pk)
            .exists()
        ):
            form.add_error(
                "name",
                "Common Area name already exists in this condominium. Please, "
                "choose a different one.",
            )
            return self.form_invalid(form)

        # associate user's condominium with common area being created
        self.object.condominium = self.request.user.condominium
        self.object.save()

        # update setup progress bar
        self.update_setup_progress()

        messages.success(self.request, "Common Area has been created successfully.")

        return HttpResponseRedirect(self.get_success_url())


class SetupCommonAreaEditView(SetupViewsWithDecors, UpdateView, SetupProgressMixin):
    context_object_name = "current_common_area"
    form_class = CommonAreaSetupForm
    http_method_names = ["post", "get"]
    model = CommonArea
    pk_url_kwarg = "common_area_id"
    success_url = reverse_lazy("condo:condo_setup_common_area_list")
    template_name = (
        "condo/pages/setup_pages/common_area/condo_setup_common_area_edit.html"
    )

    def dispatch(self, request, *args, **kwargs):
        if not CommonArea.objects.filter(
            condominium=request.user.condominium,
            pk=self.kwargs.get("common_area_id"),
        ).exists():
            messages.error(
                self.request,
                "The Common Area you're trying to edit either doesn't exist or you don't have permission to edit it.",
            )
            return redirect(reverse("condo:condo_setup_common_area_list"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # get form instance without saving it
        self.object = form.save(commit=False)

        # verify if updated common area new name already exists in user condominium
        if (
            CommonArea.objects.filter(
                name__iexact=self.object.name, condominium=self.request.user.condominium
            )
            .exclude(pk=self.object.pk)
            .exists()
        ):
            form.add_error(
                "name",
                "Common Area name already exists in this condominium. Please, choose a different one",
            )
            return self.form_invalid(form)

        # save updated common area in db
        self.object.save()

        # update setup progress bar
        self.update_setup_progress()

        messages.success(self.request, "Common Area has been updated successfully.")
        return HttpResponseRedirect(self.get_success_url())


class SetupCommonAreaDeleteView(SetupViewsWithDecors, DeleteView):
    context_object_name = "current_common_area"
    form_class = CommonAreaSetupForm
    http_method_names = ["get", "post"]
    model = CommonArea
    pk_url_kwarg = "common_area_id"
    success_url = reverse_lazy("condo:condo_setup_common_area_list")
    template_name = (
        "condo/pages/setup_pages/common_area/condo_setup_common_area_delete.html"
    )

    def dispatch(self, request, *args, **kwargs):
        """
        Handles request dispatching for the common area delete view.
        Checks if the common area with the given ID exists and belongs to the user's condominium.
        If not, displays an error message and redirects to the common area list page.
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments, including 'common_area_id'
        Returns:
            HttpResponse: Redirect to common area list if validation fails,
                          otherwise proceeds with normal dispatch flow
        """

        if not CommonArea.objects.filter(
            condominium=request.user.condominium, pk=self.kwargs.get("common_area_id")
        ).exists():
            messages.error(
                request,
                "The Common Area you're trying to delete either doesn't exist or you don't have permission to delete it.",
            )
            return redirect(reverse("condo:condo_setup_common_area_list"))
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        return super().delete(request, *args, **kwargs)

    # def form_valid(self, form):
    #     success_url = self.get_success_url()
    #     self.object.delete()
    #     messages.success(self.request, "Common Area has been deleted successfully.")
    #     return HttpResponseRedirect(success_url)
