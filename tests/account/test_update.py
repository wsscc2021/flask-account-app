"""
    TestCase of /account/{username} PUT API
    account 정보를 수정하는 API를 테스트합니다.
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

def update_account(client, path, body):
    return client.put(
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
    
    body = {
        "email": "piou987@naver.com"
    }
    response = update_account(client, path, body)
    assert response.status_code == 200

def test_content_not_found(client):
    path = "/account/test001"
    body = {
        "email": "piou987@naver.com"
    }
    response = update_account(client, path, body)
    assert response.status_code == 404