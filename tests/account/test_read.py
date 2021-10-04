"""
    TestCase of /account/{username} GET API
    account 정보를 읽어오는 API를 테스트합니다.
"""
# standard library
import json

def create_account(client, path, body):
    return client.post(
        path,
        data=json.dumps(body),
        content_type='application/json',
        follow_redirects=True 
    )

def read_account(client, path):
    return client.get(
        path,
        content_type='application/json',
        follow_redirects=True 
    )

def test(client):
    path = "/account/test001"
    body = {
        "password": "Z00keeper!2#",
        "email": "worldskills.developer@gmail.com"
    }
    response = create_account(client, path, body)
    assert response.status_code == 201
    
    response = read_account(client, path)
    assert response.status_code == 200

def test_content_not_found(client):
    path = "/account/test001"
    response = read_account(client, path)
    assert response.status_code == 404