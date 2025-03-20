from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.condo.forms import CommonAreaSetupForm
from apps.condo.models import CommonArea

from .base import SetupProgressMixin, SetupViewsWithDecors


class SetupCommonAreaListView(SetupViewsWithDecors, ListView):
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
        if not self.request.user.condominium:
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
