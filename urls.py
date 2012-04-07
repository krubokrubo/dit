from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic.simple import redirect_to
from dit import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^dit/', include('dit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^passwordchange/$', auth_views.password_change, name='auth_password_change'),
    url(r'^passwordchange/done/$', auth_views.password_change_done, name='auth_password_change_done'),
    url(r'^passwordreset/$', auth_views.password_reset, name='auth_password_reset'),
    url(r'^passwordreset/done/$', auth_views.password_reset_done, name='auth_password_reset_done'),
    url(r'^passwordreset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^passwordreset/complete/$', auth_views.password_reset_complete, name='auth_password_reset_complete'),


    url(r'^$', redirect_to, {'url':settings.FIRST_URL}),
    url(r'^dt/$', 'dit.dt.views.commitmenttable', name='commitmenttable'),
    url(r'^dt/add/$', 'dit.dt.views.commitment', name='commitmentadd'),
    url(r'^dt/(\d+)/$', 'dit.dt.views.commitment', name='commitment'),
    url(r'^dt/invite/$', 'dit.dt.views.invite', name='invite'),
)
