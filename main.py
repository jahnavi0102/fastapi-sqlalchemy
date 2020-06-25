"""
FastAPI application and endpoints
"""
import sqlalchemy as al
from pydantic import BaseModel
from fastapi import FastAPI, Response
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except KeyError as e:
    print("Using static database URL")
    DATABASE_URL = "postgres://gudilbqulmwevs:f97336e5a36fddfd605e05845fc6b9e1d37efecb1d0103accf9c42a349210586@ec2-52-202-66-191.compute-1.amazonaws.com:5432/ddbg838br74koo"


app = FastAPI()

database = al.create_engine(
    DATABASE_URL
)
connection = database.connect()

# post location request body
class mappingIn(BaseModel):
    place_name: str
    admin_name1: str
    latitude: float
    longitude: float 
    country: str = None
    pin: int


@app.on_event("startup")
def startup():
    global connection
    connection = database.connect()


@app.on_event("shutdown")
def shutdown():
    database.disconnect()


# Get the location Pincode, Address, City and Country by entering latitude and longitude::
@app.get("/get_location")
def get_map(lat : float, long: float):
    query = "SELECT * FROM mapping WHERE latitude={0} and longitude={1}".format(lat, long)
    result = connection.execute(query)
    
    count = result.rowcount
    if count <= 0:
        not_found_resp = {"status": "not found"}
        return Response(content=json.dumps(not_found_resp), status_code=404)
    
    resultset=[]
    row = "" # empty delcaration, not None
    while row is not None:
        row = result.fetchone()
        if row is not None:
            resultset.append(row)

    return resultset


# Feed location data such as lat, long, place name etc. into the postgre database::
@app.post("/post_location", response_model=mappingIn)
def insert_geo(mapping: mappingIn):
    if mapping.country is None:
        mapping.country = "IN" # default case
    
    pin = mapping.pin

    pin_check_query = "select * from mapping where pin={0}".format(pin)
    result = connection.execute(pin_check_query)
    result_count = result.rowcount
    print(result_count)
    if result_count == 1:
        # duplicate cannot exist
        already_exist_resp = {"status": "already exist"}
        return Response(content=json.dumps(already_exist_resp), status_code=400)
    else:
        try:
            result = connection.execute("INSERT INTO mapping VALUES('{0}','{1}',{2},{3},'{4}',{5});".format(mapping.place_name , mapping.admin_name1 , mapping.latitude , mapping.longitude , mapping.country , mapping.pin))
            success_resp = {"status": "successfully added"}
            return Response(content=json.dumps(success_resp), status_code=200)
        except Exception as e:
            print(e)
            database_error = {"status": "internal server error"}
            return Response(content=json.dumps(database_error), status_code=500)    


# Get data of locations in r KM (default 5Km) radius by entering the lat and long of a particular::
@app.get("/get_using_postgres")
def get_using_postgres(lat:float , long:float, radius:float = 5):
    query =  """
        SELECT * FROM (
        SELECT (
        point(m.longitude, m.latitude)<@>point({0}, {1})
        ) * 1609.344 as distance, * FROM mapping m
        ) as distances WHERE distances.distance <= {2} order by distances.distance;""".format(long, lat, radius * 1000)
    
    print(query)
    result = connection.execute(query)

    resultset=[]
    row = ""
    while row is not None:
        row = result.fetchone()
        if row is not None:
            resultset.append(row)
    
    return resultset
   

# Get data of locations in r KM (default 5Km) radius using self calculations::
@app.get("/get_using_self")
def get_using_self(lat:float , long:float, radius:float = 5):
    query =  """
        SELECT *, (acos(sin(radians({0})) * sin(radians(mapping.latitude)) + cos(radians({0})) * cos(radians(mapping.latitude)) * cos(radians(mapping.longitude) - radians({1}))) * 6371) as distance FROM mapping WHERE 
        acos(sin(radians({0})) * sin(radians(mapping.latitude)) + cos(radians({0})) * cos(radians(mapping.latitude)) * cos(radians(mapping.longitude) - radians({1}))) * 6371 <= {2} order by distance;
        """.format(lat, long, radius)
    
    print(query)
    result = connection.execute(query)

    resultset=[]
    row = "" # empty delcaration, not None
    while row is not None:
        row = result.fetchone()
        if row is not None:
            resultset.append(row)
    
    return resultset


#  It will take input as latitude + longitude, it will tell you which place it falls within::
@app.get("/detect")
def get_map(lat : float, long: float):
    query = "SELECT id, location_name, location_type, location_parent FROM geostore WHERE ST_Within(ST_GeometryFromText('SRID=4326;POINT({0} {1})'), polygon) LIMIT 1".format(long, lat)
    print(query)
    result = connection.execute(query)
    
    count = result.rowcount
    if count <= 0:
        not_found_resp = {"status": "not found"}
        return Response(content=json.dumps(not_found_resp), status_code=404)
    
    resultset=[]
    row = ""
    while row is not None:
        row = result.fetchone()
        if row is not None:
            resultset.append(row)

    return resultset
