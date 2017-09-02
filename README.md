# gis_maps
django: driving distance PoC (very rough)

Creates driving distance polygons based on user-inputted location.

Data needs to be processed beforehand. Cloning repo will not make it work.

Requirements:
- Postgres with extensions: PostGIS (geometry extension), pgrouting (djikstra street routing)
- Python 3 with extensions: psycopg2 (Postgres connector), requests (http lib)
- Django with extensions: geodjango (geometry model layer)
- google maps api key (displaying and geocoding)
- road geometry (for PoC, using: Statistics Canada 2016 Road Network geometry)

For a rough overview of how it works, check out: /test sql scripts/backend.py
For data preprocessing, check out: /test sql scripts/setup scripts.sql
To see the geojson exporter, check out: /test sql scripts/geojson_exporter.sql
