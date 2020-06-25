"""
utils for testing
"""
import os
import sqlalchemy as al

# testing data
dummy_data = {
    'status_not_found': {"status": "not found"},
    'added_successfully': {"status": "successfully added"},
    'already_exists': {"status": "already exist"},
    'test_get_location': [
                            {
                                "place_name": "Aliganj",
                                "admin_name1": "New Delhi",
                                "latitude": 28.65,
                                "longitude": 77.2167,
                                "country": "IN",
                                "pin": 110003
                            },
                            {
                                "place_name": "Rashtrapati Bhawan",
                                "admin_name1": "New Delhi",
                                "latitude": 28.65,
                                "longitude": 77.2167,
                                "country": "IN",
                                "pin": 110004
                            },
                            {
                                "place_name": "Bara Tooti",
                                "admin_name1": "New Delhi",
                                "latitude": 28.65,
                                "longitude": 77.2167,
                                "country": "IN",
                                "pin": 110006
                            },
                            {
                                "place_name": "Patel Nagar",
                                "admin_name1": "New Delhi",
                                "latitude": 28.65,
                                "longitude": 77.2167,
                                "country": "IN",
                                "pin": 110008
                            }
                        ],
    'test_post_location': {
                                "place_name": "Roorkee",
                                "admin_name1": "Uttarakhand",
                                "latitude": 29.8543,
                                "longitude": 77.8880,
                                "pin": 999999
                        },
    'test_post_location_exists': {
                                        "place_name": "Kangra H O",
                                        "admin_name1": "Himachal Pradesh",
                                        "latitude": 32.0537,
                                        "longitude": 76.2852,
                                        "pin": 176001
                                },
    'test_get_using_postgres_params': { 'lat': 28.65,
                                        'long': 77.2167
                                    },
    'test_get_using_postgres_length': 44, 
    'test_get_using_self_params': { 'lat': 28.65,
                                        'long': 77.2167
                                    },
    'test_get_using_self_length': 44,
    'test_detect_point': [
                            {
                                "id": 13,
                                "location_name": "Central Delhi",
                                "location_type": "Zone",
                                "location_parent": "Delhi"
                            }
                        ],
    'test_detect_point_params': {
                                'lat':28.630540,
                                'long': 77.219847
                            },
    'test_detect_point_not_bound_params': {
                                'lat': 00.0000,
                                'long': 00.0000
                            }
}


# delete record from mapping table using pincode detail
def delete_record_pincode(pincode):
    delete_query = "delete from mapping where pin=" + pincode
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
    except KeyError as e:
        print("Using static database URL")
        DATABASE_URL = "postgres://gudilbqulmwevs:f97336e5a36fddfd605e05845fc6b9e1d37efecb1d0103accf9c42a349210586@ec2-52-202-66-191.compute-1.amazonaws.com:5432/ddbg838br74koo"
    
    database = al.create_engine(
        DATABASE_URL
    )
    connection = database.connect()
    
    try:
        result = connection.execute(delete_query)
        return True
    except Exception as e:
        print('Unable to delete record for pin', pincode)
        return False
