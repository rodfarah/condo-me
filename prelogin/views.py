from django.shortcuts import render


def home(request):
    return render(request=request, template_name="prelogin/pages/home.html")


def faqs(request):
    return render(request=request, template_name="prelogin/pages/faqs.html")


def features(request):
    return render(request=request, template_name="prelogin/pages/features.html")


def pricing(request):
    return render(request=request, template_name="prelogin/pages/pricing.html")
