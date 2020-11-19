from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# from django.conf.urls import handler400, handler403, handler404, handler500  # noqa

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('testify/', include('testify.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# handler404 = 'core.views.error_404'
# handler400 = 'core.views.error_400'
# handler403 = 'core.views.error_403'
# handler500 = 'core.views.error_500'
