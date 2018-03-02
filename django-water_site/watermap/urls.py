from django.conf.urls import  url, include
from .views import map_data, index

urlpatterns = [
	url(r'^watermap/$', index, name = 'index'),
	url(r'^api/map_data', map_data, name = 'map_data'),
]