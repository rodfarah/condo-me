from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.prelogin.urls")),
    path("condo/", include("apps.condo.urls")),
    path("condo_people/", include("apps.condo_people.urls")),
    path("reservation/", include("apps.reservation.urls")),
    path("purchase/", include("apps.purchase.urls")),
]

if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
