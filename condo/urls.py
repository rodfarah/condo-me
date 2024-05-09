from django.urls import path
from . import views

app_name = 'condo'

urlpatterns = [
    path('', views.home, name='home')
]
