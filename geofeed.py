
import json
import sqlalchemy as al

extentions_sql = "CREATE EXTENSION IF NOT EXISTS postgis;"
polygon_sql = """
    CREATE TABLE IF NOT EXISTS geostore (
        id SERIAL PRIMARY KEY,
        location_name varchar(256),
        location_type VARCHAR(64),
        location_parent varchar(256),
        polygon GEOMETRY
    );"""
indexing_polygon_sql = """
                CREATE INDEX IF NOT EXISTS location_polygon_idx ON geostore USING GIST (polygon);
                """
insert_query = """
            INSERT INTO geostore (location_name, location_type, location_parent, polygon) VALUES ('{0}', '{1}', '{2}', ST_GeometryFromText('SRID=4326;POLYGON(({3}))'));
            """

DATABASE_URL = "postgres://bycyitptybvtsj:06fa85b8742c3ed4581993fcdbb6b33211e53a4271e884e11b21bb403e06a6b5@ec2-50-17-90-177.compute-1.amazonaws.com:5432/d7s3hiaijvira2"

database = al.create_engine(
    DATABASE_URL
)
connection = database.connect()

# run table creation and geometry indexing
result = connection.execute(extentions_sql + ';' + polygon_sql + ';' + indexing_polygon_sql)

file_name = "geodata.json"
with open(file_name) as json_file:
    content = json_file.read()
    json_data = json.loads(content)
    cities = json_data['features']

    for city in cities:
        city_properties = city['properties']
        city_geometry_details = city['geometry']

        polygon_boundaries = city_geometry_details['coordinates'][0]

        query_point_str = ''
        count = 0
        for point in polygon_boundaries:
            count += 1 
            query_point_str += str(point[0]) + ' ' + str(point[1]) # 1 is the latitude, 0 is the longitude
            if count < len(polygon_boundaries):
                query_point_str += ', '

        insert_copy = insert_query
        insert_copy = insert_copy.format(city_properties['name'], city_properties['type'], city_properties['parent'], query_point_str)

        # print(insert_copy)
        result = connection.execute(insert_copy)
        count = result.rowcount
        if count <= 0:
            not_found_resp = {"status": "not found"}
            print(not_found_resp)




