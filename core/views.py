from django.shortcuts import render


def home(request):
    return render(request=request, template_name='core/pages/home.html')


def faq(request):
    return render(request=request, template_name='core/pages/faqs.html')


def features(request):
    return render(request=request, template_name='core/pages/features.html')


def pricing(request):
    return render(request=request, template_name='core/pages/pricing.html')
