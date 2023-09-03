import pytest
import requests
import json

# URL of the API you want to test
API_URL = 'https://creditapi-joqlneigka-uc.a.run.app'

# Test if the root URL returns 'hello simon'
def test_racine():
    response = requests.get(f'{API_URL}/')
    assert 'hello simon' in str(response.text)

# Test client name (you may need to replace this with the actual API endpoint or function)
def test_client_name():
    # Implement this based on how you retrieve client names from the API
    pass

# Test if EXT_SOURCE_3 is an integer or a float
def test_EXT_SOURCE_3():
    # Query the API for EXT_SOURCE_3 and then run your assertion tests
    # For example:
    # response = requests.get(f'{API_URL}/your_endpoint_for_EXT_SOURCE_3')
    # assert isinstance(response.json()['EXT_SOURCE_3'], (int, float))
    pass

# Test if a known client ID returns EXT_SOURCE_3
def test_infos_client_known():
    payload = json.dumps({'client_id': 100002})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{API_URL}/infos_client', data=payload, headers=headers)
    data = response.json()
    print(data)
    assert 'EXT_SOURCE_3' in data

# Test if an unknown client ID returns 'inconnu'
def test_infos_client_unknown():
    payload = json.dumps({'client_id': 10067554})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{API_URL}/infos_client', data=payload, headers=headers)
    data = response.json()
    print(data)
    assert data['ID client '] == 'inconnu'

