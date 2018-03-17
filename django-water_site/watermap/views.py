from django.shortcuts import render
from watermap.models import SwaziTest
from watermap.models import SwaziMvp
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.core import serializers
import json



# Create your views here.
# index function returns the watermap dashboard
def dashboard(request):
	return render(request, 'watermap/dashboard.html')



# API call to database and returns JSON response    
def map_data(request):
    raw_data = serializers.serialize('python', SwaziTest.objects.all()[0:40], fields = ('field_water_tech', 'field_status_id'\
    	, 'field_water_source', 'field_country_name', 'field_lat_deg', \
    	'field_long_deg'))
    actual_data = [d['fields'] for d in raw_data]
    return JsonResponse(actual_data, safe= False)

# Returns the home page
def homepage(request):
    return render(request, 'watermap/index.html')

#load the team page
def team(request):
	return render(request, 'watermap/team.html')

# load solution page
def solution(request):
	return render(request, 'watermap/solution.html')

def map_preds(request):
    raw_data = serializers.serialize('python', SwaziMvp.objects.all(), fields = ('wpdx_id', 'country_name', \
    	'water_source', 'water_tech', 'status_id', 'lat_deg', 'lon_deg', 'management', 'fuzzy_water_source', \
    	'fuzzy_water_tech', 'predicted_class', 'probability', 'one_km_population', 'one_km_total_water_points', \
    	'one_km_functioning_water_points', 'impact_score', 'time_since_meas_years', 'age_well_years'))
    actual_data = [d['fields'] for d in raw_data]
    return JsonResponse(actual_data, safe= False)

