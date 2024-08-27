from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("prelogin.urls")),
    path("condo/", include("condo.urls")),
    path("condo_people/", include("condo_people.urls")),
    path("reservation/", include("reservation.urls")),
    path("purchases/", include("purchases.urls")),
]


urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
