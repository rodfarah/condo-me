from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('core/faqs', views.faq, name='faqs'),
    path('core/features', views.features, name='features'),
    path('core/pricing', views.pricing, name='pricing'),
]
