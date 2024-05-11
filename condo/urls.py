from django.urls import path
from . import views

app_name = 'condo'

urlpatterns = [
    path('', views.home, name='home'),
    path('condominium', views.condominium, name='condominium'),
    path('common_areas', views.common_areas, name='common_areas'),
]
