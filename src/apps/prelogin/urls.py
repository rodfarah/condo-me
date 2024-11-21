from django.urls import path

from . import views

app_name = "apps.prelogin"

urlpatterns = [
    path("", views.home, name="home"),
    path("faqs/", views.faqs, name="faqs"),
    path("features/", views.features, name="features"),
    path("pricing/", views.pricing, name="pricing"),
    path("about/", views.about, name="about"),
]
