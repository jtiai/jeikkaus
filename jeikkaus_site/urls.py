from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^$', 'jeikkaus.views.match_list'),
    (r'^jeikkaus/', include('jeikkaus.urls')),
    (r'^login/$', 'django.contrib.auth.views.login', None, 'login'),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login', { 'login_url' : '/' }, 'logout'),
    (r'^password_change/$', 'django.contrib.auth.views.password_change', None, 'change_password'),
    (r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', None, 'password_change_done'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
