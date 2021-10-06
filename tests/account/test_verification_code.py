"""
    TestCase of /account/{username}/verification_code POST API
    account 활성화를 위한 인증코드를 생성하는 API를 테스트합니다.
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

def create_verification_code(client, path):
    return client.post(
        path,
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

    path = "/account/test001/verification_code"
    response = create_verification_code(client, path)
    assert response.status_code == 201

def test_no_account(client):
    path = "/account/nouser001/verification_code"
    response = create_verification_code(client, path)
    assert response.status_code == 404