from django.shortcuts import render


def home(request):
    return render(request, "prelogin/pages/home.html")


def faqs(request):
    return render(request, "prelogin/pages/faqs.html")


def features(request):
    return render(request, "prelogin/pages/features.html")


def pricing(request):
    return render(request, "prelogin/pages/pricing.html")


def about(request):
    return render(request, "prelogin/pages/about.html")
