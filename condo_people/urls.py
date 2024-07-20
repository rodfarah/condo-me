from django.urls import path

from . import views

app_name = 'condo_people'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path(
        'register/success', views.register_success,
        name='success'),
]
