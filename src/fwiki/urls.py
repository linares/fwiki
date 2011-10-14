from django.conf.urls.defaults import patterns, include, url
from fwiki import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       
    url(r'^login$', 'fwiki.taxonomy.views.user_login'),
    #url(r'^fb_login$', 'fwiki.taxonomy.views.fb_login'),
    url(r'^$', 'fwiki.taxonomy.views.index'),    #/ => show a home page
    url(r'^_xhr/(?P<endpoint>.*)$', 'fwiki.taxonomy.xhr.login.distrib'),
    url(r'^places/(?P<node_id>[a-z]{2}\/\w+)$', 'fwiki.taxonomy.views.render_node'),  #/places/_en_paris => show a Paris page with aggregate context
    url(r'^(?P<username>\w+)$', 'fwiki.taxonomy.views.render_user' ),   #/alex => show my landing page
    url(r'^(?P<username>\w+)/(?P<node_id>.*)$', 'fwiki.taxonomy.views.render_usernode'),   #/alex/_en_paris  => show my paris page with context

    # url(r'^fwiki/', include('fwiki.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)