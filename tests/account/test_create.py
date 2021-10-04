"""
    TestCase of /account/{username} DELETE API
    account 를 생성하는 API를 테스트합니다.
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

def test(client):
    path = "/account/test001"
    body = {
        "password": "Z00keeper!2#",
        "email": "worldskills.developer@gmail.com"
    }
    response = create_account(client, path, body)
    assert response.status_code == 201

def test_duplicate_username(client):
    path = "/account/test001"
    body = {
        "password": "Z00keeper!2#",
        "email": "worldskills.developer@gmail.com"
    }
    response = create_account(client, path, body)
    assert response.status_code == 201
    response = create_account(client, path, body)
    assert response.status_code == 403

def test_bad_request_password(client):
    path = "/account/test001"
    body = {
        "no-password": "Z00keeper!2#",
        "email": "worldskills.developer@gmail.com"
    }
    response = create_account(client, path, body)
    assert response.status_code == 400

def test_bad_request_email(client):
    path = "/account/test001"
    body = {
        "password": "Z00keeper!2#",
        "no-email": "worldskills.developer@gmail.com"
    }
    response = create_account(client, path, body)
    assert response.status_code == 400