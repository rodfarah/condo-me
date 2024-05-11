from django.shortcuts import render


def home(request):
    return render(request=request, template_name='condo/pages/home.html')


def condominium(request):
    return render(request=request,
                  template_name='condo/pages/condominium.html')


def common_areas(request):
    return render(request, 'condo/pages/common_areas.html')
