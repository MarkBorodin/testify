from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

API_PREFIX = 'api/v1'

urlpatterns = [

    # UI
    path('admin/', admin.site.urls, name='admin'),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('testify/', include('testify.urls')),

    # API
    path(f'{API_PREFIX}/testify/', include('testify.api.urls')),
    path(f'{API_PREFIX}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{API_PREFIX}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
