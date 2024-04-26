from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', include('core.urls'))
]


urlpatterns += static(prefix=settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(prefix=settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
