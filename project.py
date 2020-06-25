"""
Script for processing location, places data from CSV and storing into Postgres table `mapping`
"""
import psycopg2
import pandas as pd
import csv
import os
from urllib.parse import urlparse

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except KeyError as e:
    print("Using static database URL")
    DATABASE_URL = "postgres://gudilbqulmwevs:f97336e5a36fddfd605e05845fc6b9e1d37efecb1d0103accf9c42a349210586@ec2-52-202-66-191.compute-1.amazonaws.com:5432/ddbg838br74koo"

parsed_url = urlparse(DATABASE_URL)

conn = psycopg2.connect(
        database = parsed_url.path[1:],
        user = parsed_url.username,
        password = parsed_url.password,
        host = parsed_url.hostname
        )


def create_table():
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS mapping(
                place_name text,
                admin_name1 text,
                latitude float,
                longitude float,
                country text ,
                pin integer PRIMARY KEY
                )""")
    conn.commit()


def insert(place_name , admin_name1 , latitude , longitude , Country , pin):
    if ( not str(latitude) or 
        not str(longitude) or 
        not str(pin) or 
        not str(place_name) or 
        not str(admin_name1)):
        return
    
    cur = conn.cursor() 
    cur.execute("INSERT INTO mapping(place_name , admin_name1 , latitude , longitude , Country , pin) VALUES(%s,%s,%s,%s,%s,%s);" , (place_name , admin_name1 , latitude , longitude , Country , pin))   
    conn.commit()

create_table()
data = pd.read_csv("data/IN.csv") 
pincode = data["key"].str.split("/", n = 1, expand = True) 
data["Country"]= pincode[0] 
data["pin"]= pincode[1]
data.drop(columns =["key"], inplace = True) 
data.drop(columns =["accuracy"], inplace = True)

df = pd.DataFrame(data)  
df.to_csv("data/OUT.csv", index=False)
  

with open("data/OUT.csv", 'r') as f:
    reader = csv.reader(f)
    columns = next(reader)
    # f.seek(0)
    count = 0
    for row in reader:
        print(count)
        count += 1
        my_row = row
        place_name = my_row[0]
        admin_name1 = my_row[1]
        latitude = my_row[2]
        longitude = my_row[3]
        Country = my_row[4]
        pin = my_row[5]
        insert(place_name , admin_name1 , latitude , longitude , Country , pin)
    
    conn.close()
