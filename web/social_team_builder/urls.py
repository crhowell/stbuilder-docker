from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import notifications.urls


urlpatterns = [
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^users/', include('profiles.urls', namespace='profiles')),
    url(r'^me/notifications/', include('notifications.urls', namespace='notifications')),
    url(r'^', include('projects.urls', namespace='projects')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
