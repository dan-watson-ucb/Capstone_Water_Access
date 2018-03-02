from django.shortcuts import render
from watermap.models import SwaziTest
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.
def index(request):
	Swazcount = SwaziTest.objects.filter(row_id__contains = 472293)
	return render(request, 'watermap/home.html')




def map_data(request):
    output = SwaziTest.objects.all()[0:10]
    output = serializers.serialize('json', output, fields = ('field_water_tech', 'field_status_id'\
    	, 'field_water_source', 'field_country_name', 'field_lat_deg', \
    	'field_long_deg'))
    return HttpResponse(output, content_type = "application/json")

