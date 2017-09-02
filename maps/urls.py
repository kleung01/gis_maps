from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.map_index, name='map_index'),
	url(r'^add/',views.get_location, name='get_location'),
]

