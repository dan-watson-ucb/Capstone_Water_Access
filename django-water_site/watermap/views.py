from django.shortcuts import render
from watermap.models import SwaziTest
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.core import serializers
import json



# Create your views here.
def index(request):
	Swazcount = SwaziTest.objects.filter(row_id__contains = 472293)
	return render(request, 'watermap/home.html')




'''def map_data(request):
    output = serializers.serialize('json', SwaziTest.objects.all()[0:10], fields = ('field_water_tech', 'field_status_id'\
    	, 'field_water_source', 'field_country_name', 'field_lat_deg', \
    	'field_long_deg'))
    return JsonResponse(output, safe= False)'''


    
def map_data(request):
    raw_data = serializers.serialize('python', SwaziTest.objects.all()[0:1000], fields = ('field_water_tech', 'field_status_id'\
    	, 'field_water_source', 'field_country_name', 'field_lat_deg', \
    	'field_long_deg'))
    actual_data = [d['fields'] for d in raw_data]
    return JsonResponse(actual_data, safe= False)

