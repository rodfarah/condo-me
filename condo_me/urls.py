from django.urls import path
from condo_me import views

app_name = 'condo_me'

urlpatterns = [
    path('', views.home, name='home'),
]
