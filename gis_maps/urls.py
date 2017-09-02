from django.conf.urls import include,url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^maps/', include('maps.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^add/', include('maps.urls'))
]

# serve static files
urlpatterns += staticfiles_urlpatterns()