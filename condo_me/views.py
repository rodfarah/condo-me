from django.shortcuts import render

def home(request):
    return render(request=request, template_name='condo_me/pages/home.html')

def faq(request):
    return render(request=request, template_name='condo_me/pages/faqs.html')

def features(request):
    return render(request=request, template_name='condo_me/pages/features.html')