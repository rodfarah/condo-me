from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('user/register/success', views.register_success, name='success'),
]
