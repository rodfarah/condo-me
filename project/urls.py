from django.urls import path
from condo_me import views

urlpatterns = [
    path('', views.home, name='home')
]
