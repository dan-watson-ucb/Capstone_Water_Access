from django.conf.urls import  url, include
from .views import map_data, dashboard, homepage, team, solution, map_preds

urlpatterns = [
	url(r'^dashboard$', dashboard, name = 'dashboard'),
	url(r'^api/map_data$', map_data, name = 'map_data'),
	url(r'^$', homepage, name = 'home'),
	url(r'^team$', team, name = 'team'),
	url(r'^solution$', solution, name = 'solution'),
	url(r'^api/map_preds$', map_preds, name = "map_preds")


]