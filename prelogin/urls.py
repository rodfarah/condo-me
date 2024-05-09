from django.urls import path
from prelogin import views

app_name = 'prelogin'

urlpatterns = [
    path('', views.home, name='home'),
    path('prelogin/faqs', views.faq, name='faqs'),
    path('prelogin/features', views.features, name='features'),
    path('prelogin/pricing', views.pricing, name='pricing'),
]
