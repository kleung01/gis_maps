# makes rfc7946 compatible geojson
# requires postgres+postgis for coordinate features
# replace maps_dd_node with your table
# add whatever properties (substitute cost_seconds)
# add whatever condition (substitute session)

SELECT json_build_object (
	'type', 'FeatureCollection',
	'features', json_agg(
		json_build_object(
			'type', 'Feature',
			'geometry', json_build_object(
				'type', 'Point',
				'coordinates', array[ST_X(the_geom)::float, ST_Y(the_geom)::float]
			),
			'properties', json_build_object(
				'cost_seconds', round(cost::numeric*60)
			)
		)
	)
)
FROM maps_dd_node
WHERE session = '0001';

# for python
SELECT json_build_object ('type', 'FeatureCollection', 'features', json_agg(json_build_object('type', 'Feature', 'geometry', json_build_object('type', 'Point', 'coordinates', array[ST_X(the_geom)::float, ST_Y(the_geom)::float] ), 'properties', json_build_object('cost_seconds', round(cost::numeric*60) ) ) ) ) FROM maps_dd_node WHERE session = '{}';