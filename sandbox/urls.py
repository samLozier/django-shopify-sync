from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from django.conf import settings
import os

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))

