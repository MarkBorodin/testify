from django.urls import path

from . import views

# from django.conf.urls import handler400, handler403, handler404, handler500 # noqa

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    ]

handler404 = views.error_404
handler400 = views.error_400
handler403 = views.error_403
handler500 = views.error_500
