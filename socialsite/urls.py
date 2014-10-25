from django.conf.urls import patterns, include, url
from login.views import *
from posts.views import *
from friends.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'socialsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', 'django.contrib.auth.views.login'),
    #url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^login/$', login_view),
    url(r'^login_success/$', login_success),
    url(r'^login_notsuccess/$', login_notsuccess),
    url(r'^updatepost/$', update_post),
    url(r'^send_request/$',send_request),
    url(r'^get_friend_requests/$',get_friend_requests),
    url(r'^accept_request/$',accept_request),
    url(r'^reject_request/$',reject_request),
    url(r'^logout/$',logout_view),
    url(r'^autocompleteusers_name/$',autocompleteusers_name),
    url(r'^autocompleteusers_email/$',autocompleteusers_email),
    url(r'^get_all_friends/$',get_all_friends),
    url(r'^get_all_posts/$',get_all_posts),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'registration/password_change_form.html','post_change_redirect':'/login_success'}),
    #url(r'^password_change_done/$','django.contrib.auth.views.password_change_done', {'template_name': 'registration/password_change_done.html'}),
    #url(r'^home/$', home),
)
