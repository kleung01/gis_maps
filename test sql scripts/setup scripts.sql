# verbosity postgres
sublime  /usr/local/var/postgres/postgresql.conf
log_min_messages = debug5
log_min_error_statement = debug5
log_min_duration_statement = -1
brew services restart postgresql

# setup db: installs postgis, pgrouting, postgis
brew install pgrouting

# setting up db: postgres9.6
CREATE DATABASE pg_django;
CREATE USER kev WITH PASSWORD 'helloworld';
ALTER ROLE kev SET client_encoding TO 'utf8';
ALTER ROLE kev SET default_transaction_isolation TO 'read committed';
ALTER ROLE kev SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE pg_django TO kev;
CREATE EXTENSION POSTGIS;
CREATE EXTENSION PGROUTING;


# configure django settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pg_django',
        'USER': 'kev',
        'PASSWORD': 'helloworld',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# setup geodjango
'ENGINE': 'django.contrib.gis.db.backends.postgis'

# geodjango: libgeos.py is broken, regex is failing. goto site-packages/django/contrib/gis/geos/libgeos.py
ver = geos_version().decode().split(' ')[0]

# transfer from to_roads maps_model
insert into maps_roads (id, ngduid, source, target, speed_kmh, dist_km, cost_min, street_type, the_geom)
	select id, ngduid::INTEGER, source, target, speed_kmh, length_km as "speed_kmh", time_min as cost_min, type as street_type, geom as the_geom
	from toronto_roads;

insert into maps_node (id, cnt, chk, ein, eout, the_geom)
	select id, cnt, chk, ein, eout, the_geom
	from maps_roads_vertices_pgr;

# set SOURCE and TARGET = Null, do it to redo createNodes()
update maps_roads
	set Source = Null;

update maps_roads
	set Target = Null;

# make nodes
select pgr_createTopology('maps_roads', 0.0001, 'the_geom', 'id');


# configuring django to use postgres
python3 manage.py migrate
python3 manage.py createsuperuser
pw: !n9KjDnXedi0A7XmCfjgGz*ygtx&U#P$Fl%8x@tRB6l&$rcPqv8UvT3y121FhE&E2u$y@CB4tJSo4Keq%aredaCGUV#q*kJELrfD
gmaps_api_key: 'AIzaSyAgoj_dYztf4eeXTvhDIcwgFjMlFOViKEU'
gmaps_ip: '60.50.145.118'

# geom
canada road network files

# set speeds
UPDATE toronto_roads
	SET speed = 100
	where class in ('10','11','12');

# line segment lengths
alter table toronto_roads
add column length_km

# projection is in metres
update toronto_roads
	set length_km = st_length(geom)/1000


# loading layers to db: lazy way
qgis -> db manager -> import layer -> create spatial index


# road geom
alter table network.publictransport add column source integer;
alter table network.publictransport add column target integer;
select pgr_createTopology('toronto_roads', 0.0001, 'geom', 'id');

# testing djikstra from node 1 to 2
SELECT 	seq, id1 AS node,
		id2 AS edge,
		cost,
		geom
FROM 	pgr_dijkstra(
			'SELECT 	id,
						source,
						target,
						st_length(geom) as cost
			FROM vienna_roads',
			1, 2, false, false) as di
JOIN	vienna_roads pt
ON 		di.id2 = pt.id;




