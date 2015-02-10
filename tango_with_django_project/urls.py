from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView

#createa a new class that redirects the user to the index page, if succesful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(selfself, request, user):
        return '/rango/'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')), #sends 'rango/' string to rango/urls.py, which then sends request to rango/view.py, which dispatches index()
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    (r'^accounts/', include('registration.backends.simple.urls')),
)

#if settings.py has DEBUG set to TRUE, append additional URL matching pattern to 'urlpatterns'
# urlpattern states that for any file requested with a URL starting with 'media/', the request
# will be passed to the django.views.static view. This view handles the dispatching of uploaded media files.
if settings.DEBUG: 
	urlpatterns += patterns( 
		'django.views.static',
		(r'^media/(?P<path>.*)',
		'serve',
		{'document_root': settings.MEDIA_ROOT}), )
