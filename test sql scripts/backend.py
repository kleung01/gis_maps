	'''
python PoC to imitate full website
kevin leung
polygons (alpha): https://anitagraser.com/2011/09/25/a-closer-look-at-alpha-shapes-in-pgrouting/
catchment area: https://anitagraser.com/2011/05/13/catchment-areas-with-pgrouting-driving_distance/


todo:
clear memory (del)
set driving limit to 1 hour to avoid server fire
add error handling/raise exception
'''

import requests
import json
import psycopg2

# connection details: pg_django
conn = psycopg2.connect("dbname=pg_django user=Kev host=localhost port=5432")

# gmaps_vars
addr = 'Royal Ontario Museum'
gmaps_key = 'AIzaSyDAgDcjJhon534_kvFgFd0cTsSHWAUtGM0'
gmaps_geocode = 'https://maps.googleapis.com/maps/api/geocode/json'
lang = 'en-GB'

# db_vars
drive_time = 7

#gmaps_geocoding
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

# connect to pg_django
cur = conn.cursor()

# ST_Distance format: (loc_lng loc_at)
# add EH: fail if None type
cur.execute("SELECT id, ST_Distance(the_geom,'SRID=4326;POINT(%s %s)') as dist_km FROM toronto_roads_vertices_pgr ORDER BY dist_km ASC LIMIT 1;",(loc_lng,loc_lat))
node = cur.fetchone()[0] 

# drop toronto_road_dd if exists
# add EH: fail if not exist, psycopg2.ProgrammingError
# cur.execute("DROP TABLE toronto_road_dd;")
# cur.commit()

# dd_nodes (drive distance)
cur.execute("CREATE TABLE toronto_road_dd AS (SELECT * FROM toronto_roads_vertices_pgr as a	JOIN (SELECT * FROM pgr_drivingDistance('SELECT id, source, target, time_min::float8 as cost, time_min::float8 as reverse_cost FROM toronto_roads',%s, %s)) as b ON a.id = b.node);",(node,drive_time))
conn.commit()

# drop toronto_road_dd_poly if exists
# add EH: fail if not exist, psycopg2.ProgrammingError
# cur.execute("DROP TABLE toronto_road_dd_poly;")
# cur.commit()

# dd_poly
cur.execute("CREATE TABLE toronto_road_dd_poly AS (SELECT pgr_pointsAsPolygon(' SELECT id::integer, ST_X(the_geom)::float AS x, ST_Y(the_geom)::float AS y FROM toronto_road_dd'));")
conn.commit()

# pgr_pointsAsPolygon bug: does not assign SRID
cur.execute("SELECT UpdateGeometrySRID('toronto_road_dd_poly','pgr_pointsaspolygon',4326);")
conn.commit()

# close db
cur.close()
conn.close()




