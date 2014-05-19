from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^angular$', 'app.views.angular', name='angular'),
    url(r'^node_api$', 'app.views.node_api', name='node_api'),
    url(r'^user_info$', 'app.views.user_info', name='user_info'),
    url(r'^start_game$', 'app.views.start_game', name='start_game'),
    url(r'^make_move$', 'app.views.make_move', name='make_move'),
    url(r'^abandon_game', 'app.views.abandon_game', name='abandon_game'),
    url(r'^current_game', 'app.views.current_game', name='current_game'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
