from django.urls import path
from condo import views

app_name = 'condo'

urlpatterns = [
    path('', views.home, name='home'),
    path('condo/faqs', views.faq, name='faqs'),
    path('condo/features', views.features, name='features'),
    path('condo/pricing', views.pricing, name='pricing'),
]
