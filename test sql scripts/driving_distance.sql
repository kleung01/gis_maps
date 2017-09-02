# drive time polygons
# requires road network topology (lines and nodes) as TORONTO_ROADS
# requires cost function: driving time (distance/speed)
# nearest neighbour to nearest node
# toronto_road_dd: from node 24593, 10 min drivetime cost and reverse_cost (both directions), joins to nodes
# toronto_road_dd_poly: alpha-shape polygon
# pgr_pointsAsPolygon is bugged and requires manually updating SRID

# test: moonbeam cafe: 43.6542657,-79.4023663

# make sure everything is WGS84: statscan releases in SRID: 3347
ALTER TABLE toronto_roads_vertices_pgr
    ALTER COLUMN geom TYPE geometry(Point,4326) USING ST_Transform(geom,4326);

# nn_search, closest node from coordinate
# ST_Distance args: lon,lat
SELECT id,
       ST_Distance(the_geom,'SRID=4326;POINT(-79.4023663 43.6542657)') as dist_km
FROM toronto_roads_vertices_pgr
ORDER BY dist_km ASC
LIMIT 1;

returns:
id		dist_km
25426	0.00041412899525241655

# make dd_nodes: 15 min drive
CREATE TABLE toronto_road_dd AS (
	SELECT *
	FROM toronto_roads_vertices_pgr as a
	JOIN (
		SELECT * FROM pgr_drivingDistance(
	        'SELECT id,
	        		source,
	        		target,
	        		time_min::float8 as cost,
	        		time_min::float8 as reverse_cost
	        FROM toronto_roads',
	        25426, 15)) as b
	ON a.id = b.node
);

# make dd_polygon
CREATE TABLE toronto_road_dd_poly AS (
	SELECT pgr_pointsAsPolygon('
		SELECT 	id::integer,
				ST_X(the_geom)::float AS x,
				ST_Y(the_geom)::float AS y
	    FROM 	toronto_road_dd')
);

# add SRID to dd_polygon
select UpdateGeometrySRID('toronto_road_dd_poly','pgr_pointsaspolygon',4326);

