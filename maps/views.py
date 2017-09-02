# add EH
# put geo functions to geo.py

import requests
import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db import connection

from .forms import MapsForm
from .models import userInput, node
from .geo import *

def get_location(request):
	if request.method == 'POST':
		loc = str(request.POST.get('location_field'))
		dt = int(request.POST.get('drivetime'))
		radio = str(request.POST.get('radiochoice'))
		#b = userInput(address=loc)
		#b.save()
	# start_coord: tuple (lat,lng)
	start_coord = gmaps_coord(loc)
	# start_node: tuple(node,dist)
	start_node = nearest_node(start_coord)
	# clear state: ADD SESSION COMPATIBILITY LATER
	debug_truncate()
	# hardcoded session: ADD SESSION COMPATIBILITY LATER
	dd_nodes('0001',start_node[0],dt)
	# poly
	dd_poly('0001')
	# export
	if radio=='poly':
		toGeoJson('0001','poly')
		# render page
		template = loader.get_template('map/results_poly.html')
		return render(request, 'map/results_poly.html')
	else:
		toGeoJson('0001','nodes')
		# render page
		template = loader.get_template('map/results_nodes.html')
		return render(request, 'map/results_nodes.html')
	

# takes user_input and returns tuple: (lat, lng)
def gmaps_coord(user_input):
	# gmaps_vars
	addr = user_input
	gmaps_key = 'AIzaSyDAgDcjJhon534_kvFgFd0cTsSHWAUtGM0'
	gmaps_geocode = 'https://maps.googleapis.com/maps/api/geocode/json'
	lang = 'en-GB'

	gmaps_params = {
		'address':addr,
		'key':gmaps_key,
		'language':lang
	}

	# take address
	gmaps_request = (requests.get(gmaps_geocode, params=gmaps_params)).text
	gmaps_json = json.loads(gmaps_request)

	# dict_keys(['address_components', 'formatted_address', 'geometry', 'place_id', 'types'])
	loc_formatted_addr = gmaps_json['results'][0]['formatted_address']
	loc_lat = gmaps_json['results'][0]['geometry']['location']['lat']
	loc_lng = gmaps_json['results'][0]['geometry']['location']['lng']

	return (loc_lat,loc_lng)

# expects in format: (loc_lat,loc_lng)
def nearest_node(tuple_coord):
	cur = connection.cursor()
	loc_lat,loc_lng  = tuple_coord[0],tuple_coord[1]
	node_query = "SELECT id, ST_Distance(the_geom,'SRID=4326;POINT({} {})') as node_dist_km FROM maps_node ORDER BY node_dist_km ASC LIMIT 1;".format(loc_lng,loc_lat)
	cur.execute(node_query)
	temp = cur.fetchone()
	return (temp[0],temp[1])	# node:[0] distance:[1]
	cur.close()

def dd_nodes(session, node_id, drive_time):
	cur = connection.cursor()
	dd_nodes_query = "INSERT INTO maps_dd_node (id, session, edge, cost, agg_cost, the_geom) SELECT id,'{}' AS session,edge,cost,agg_cost,the_geom FROM maps_node AS a JOIN (SELECT * FROM pgr_drivingDistance('SELECT id,source,target,cost_min::float8 as cost,cost_min::float8 as reverse_cost FROM maps_roads',{},{})) as b ON a.id = b.node".format(session,node_id,drive_time)
	cur.execute(dd_nodes_query)
	cur.close()

def dd_poly(session):
	cur = connection.cursor()
	cur.execute("CREATE OR REPLACE VIEW poly AS SELECT ST_ConcaveHull(ST_COLLECT(the_geom),0.99,false) from maps_dd_node;")
	cur.execute("INSERT INTO maps_dd_poly (pgr_pointsaspolygon,session) SELECT st_concavehull AS pgr_pointsaspolygon, '{}' AS session FROM poly;".format(session))
	cur.close()

def toGeoJson(session,type):
	if type=='poly':
		cur = connection.cursor()
		#query = "SELECT ST_AsGeoJSON(ST_ForceRHR(pgr_pointsaspolygon)) from maps_dd_poly WHERE session='{}';".format(session)
		#query = "SELECT json_build_object('type', 'FeatureCollection', 'features', json_agg(json_build_object('type',       'Feature','geometry',ST_AsGeoJSON(ST_ForceRHR(pgr_pointsaspolygon))::json, 'properties', jsonb_set(row_to_json(maps_dd_poly)::jsonb,'{geom}','0',false) ) ) ) from maps_dd_poly;"
		query="SELECT json_build_object('type', 'FeatureCollection', 'features', json_agg(json_build_object('type','Feature', 'geometry',ST_AsGeoJSON(ST_ForceRHR(pgr_pointsaspolygon))::json ) ) ) from maps_dd_poly;"
		cur.execute(query)
		temp = cur.fetchone()[0]
		export_json = json.dump(temp,open('maps/static/maps/results_poly.geojson','w'))
		cur.close()
		#with open('maps/static/maps/results_poly.geojson','w') as export_json:
		#	export_json.write(temp)

	elif type=='nodes':
		cur = connection.cursor()
		query = "SELECT json_build_object ('type', 'FeatureCollection', 'features', json_agg(json_build_object('type', 'Feature', 'geometry', json_build_object('type', 'Point', 'coordinates', array[ST_X(the_geom)::float, ST_Y(the_geom)::float] ), 'properties', json_build_object('cost_seconds', round(cost::numeric*60) ) ) ) ) FROM maps_dd_node WHERE session = '{}';".format(session)
		cur.execute(query)
		temp = cur.fetchone()[0]
		# export json
		export_json = json.dump(temp,open('maps/static/maps/results_nodes.geojson','w'))
		cur.close()

def debug_truncate():
	cur = connection.cursor()
	cur.execute("truncate maps_dd_node;")
	cur.execute("truncate maps_dd_poly;")
	cur.close()

def map_index(request):
	#return HttpResponse('hello')
	template = loader.get_template('map/render.html')
	return render(request, 'map/render.html')

