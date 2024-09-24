from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from condo.forms import CondoSetupForm


# Create a 'manager group required' decorator
def manager_group_required(view_func):
    """
    This decorator checks if user belongs to 'manager' group
    """

    def check_group(user):
        if user.groups.filter(name="manager").exists():
            return True
        raise Http404("You don't have manager permissions to access this page.")

    return user_passes_test(check_group)(view_func)


# Create a class that applies login_required and manager_group_required decoators
class SetupViewsWithDecors(View):
    """
    This class is created in order to apply login_required and manager_group_required
    to all setup areas CBVs avoiding DRY.
    """

    @method_decorator(
        login_required(
            redirect_field_name="redirect_to", login_url="/condo_people/login"
        )
    )
    @method_decorator(manager_group_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SetupAreaView(SetupViewsWithDecors):
    template_name = "condo/pages/setup_pages/setup_area.html"

    def get(self, request):
        return render(request, self.template_name)


class SetupCondominiumView(SetupViewsWithDecors):
    template_name = "condo/pages/setup_pages/setup_condominium.html"

    def get(self, request):
        form = CondoSetupForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = CondoSetupForm(data=request.POST, files=request.FILES or None)
        if form.is_valid():
            condominium = form.save()
            user = request.user
            user.condominium = condominium
            user.save()
            return HttpResponse(
                "Novo condomínio criado, verificar se foi atribuido ao user."
            )
        return render(request, self.template_name, context={"form": form})
