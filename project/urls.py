from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('prelogin.urls')),
    path('condo/', include('condo.urls'))
]


urlpatterns += static(prefix=settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(prefix=settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
