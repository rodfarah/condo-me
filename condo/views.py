from django.shortcuts import render


def home(request):
    return render(request=request, template_name='condo/pages/home.html')


def faq(request):
    return render(request=request, template_name='condo/pages/faqs.html')


def features(request):
    return render(request=request, template_name='condo/pages/features.html')


def pricing(request):
    return render(request=request, template_name='condo/pages/pricing.html')
