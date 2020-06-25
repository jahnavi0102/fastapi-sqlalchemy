from fastapi.testclient import TestClient
from main import app
from utils import dummy_data
import utils

client = TestClient(app)


# get location test for existing latitude, longitude
def test_get_location():

    test_name = 'test_get_location'
    response = client.get('/get_location?lat=28.65&long=77.2167')
    print(response)
    assert response.status_code == 200
    assert response.json() == dummy_data[test_name]


# get location test for wrong latitude, longitude
def test_get_location_false():

    test_name = 'test_get_location_false'
    response = client.get('/get_location?lat=00&long=00')
    print(response)
    assert response.status_code == 404
    assert response.json() == dummy_data['status_not_found']


# post location test for new location
def test_post_location():

    test_name = 'test_post_location'
    response = client.post('/post_location', json=dummy_data[test_name])
    assert response.status_code == 200
    assert response.json() == dummy_data['added_successfully']
    assert utils.delete_record_pincode(str(dummy_data[test_name]['pin']))


# post location test for existing location
def test_post_location_exists():

    test_name = 'test_post_location_exists'
    response = client.post('/post_location', json=dummy_data[test_name])
    assert response.status_code == 400
    assert response.json() == dummy_data['already_exists']


# test of get nearby places within a distance, using postgres earthdistance
def test_get_using_postgres():

    test_name = 'test_get_using_postgres'
    response = client.get('/get_using_postgres', params=dummy_data[test_name + '_params'])
    assert response.status_code == 200
    assert len(response.json()) == dummy_data[test_name + '_length']


# test of get nearby places within a distance, using lat long distance calculation
def test_get_using_self():

    test_name = 'test_get_using_self'
    response = client.get('/get_using_self', params=dummy_data[test_name + '_params'])
    assert response.status_code == 200
    assert len(response.json()) == dummy_data[test_name + '_length']


# testing both APIs and comparing results, for get get nearby places within a distance
def test_get_using_both_same():

    test_name = 'test_get_using_self'
    response_self = client.get('/get_using_self', params=dummy_data[test_name + '_params'])
    
    test_name = 'test_get_using_postgres'
    response_postgres = client.get('/get_using_postgres', params=dummy_data[test_name + '_params'])

    assert len(response_self.json()) == len(response_postgres.json())


# test detect point, in which place this point falls in
def test_detect_point():

    test_name ='test_detect_point'
    response= client.get('/detect', params=dummy_data[test_name + '_params'])
    
    assert response.status_code == 200
    assert response.json()[0]['location_parent'] == dummy_data[test_name][0]['location_parent'] # can't check whole response body, because ID of row might differ


# test detect point, for the case when no place bounds a point
def test_detect_point_not_bound():

    test_name = 'test_detect_point_not_bound'
    response = client.get('/detect', params=dummy_data[test_name + '_params'])

    assert response.status_code == 404
    assert response.json() == dummy_data['status_not_found']
