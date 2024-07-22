from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    if 'register_form_data' in request.session:
        del request.session['register_form_data']
    return render(
        request,
        'condo_people/pages/register.html',
        context={
            'form': form,
        }
    )


def register_create(request):
    if request.method != 'POST':
        raise Http404()

    form = RegisterForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'You are now registered, please log in.')
        request.session.pop('register_form_data', None)
        return redirect('condo_people:login')
    else:
        request.session['register_form_data'] = request.POST
        return redirect(to='condo_people:register')


def login(request):
    return render(request, 'condo_people/pages/login.html')
