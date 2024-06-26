from django.urls import path
from . import views

app_name = 'prelogin'

urlpatterns = [
    path('', views.home, name='home'),
    path('faqs', views.faq, name='faqs'),
    path('features', views.features, name='features'),
    path('pricing', views.pricing, name='pricing'),
]
