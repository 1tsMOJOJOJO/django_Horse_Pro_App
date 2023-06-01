from django.urls import path, re_path
from horse_show import views
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # enable the admin and admin docs
    path('admin/', admin.site.urls),

    # The main index
    path('', lambda r: HttpResponseRedirect('/HSPro/')),
    path('HSPro/', views.index),
    re_path(r'^HSPro/(?P<show_id>[0-9]+)/$', views.list_classes, name='list-classes'),
    re_path(r'^HSPro/(?P<show_id>[0-9]+)/classes/(?P<class_id>[0-9]+)/print/$', views.print_class),
    re_path(r'^HSPro/(?P<show_id>[0-9]+)/classes/(?P<class_id>[0-9]+)/print_split/$', views.print_split_class),
    re_path(r'^HSPro/(?P<show_id>[0-9]+)/riders/(?P<ridernum>[0-9a-zA-Z]*)/welcome/$', views.print_rider_sheet),

    path('HSPro/shows/json/', views.api_get_shows),
    re_path(r'^HSPro/shows/(?P<show_id>[0-9]+)/json/$', views.api_show),
    re_path(r'^HSPro/shows/(?P<show_id>[0-9]+)/entryimport/$', views.csv_import),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)