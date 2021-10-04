"""
    TestCase of /auth POST API
    사용자 인증을 통해 JWT 토큰을 발급받는 API를 테스트 합니다.
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
def authenticate(client, body):
    return client.post(
        "/auth",
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
        "username": "test001",
        "password": "Z00keeper!2#"
    }
    response = authenticate(client, body)
    assert response.status_code == 201

def test_bad_request_username(client):
    path = "/account/test001"
    body = {
        "password": "Z00keeper!2#",
        "email": "worldskills.developer@gmail.com"
    }
    response = create_account(client, path, body)
    assert response.status_code == 201

    body = {
        "no-username": "test001",
        "password": "Z00keeper!2#"
    }
    response = authenticate(client, body)
    assert response.status_code == 400

def test_bad_request_password(client):
    path = "/account/test001"
    body = {
        "password": "Z00keeper!2#",
        "email": "worldskills.developer@gmail.com"
    }
    response = create_account(client, path, body)
    assert response.status_code == 201

    body = {
        "username": "test001",
        "no-password": "Z00keeper!2#"
    }
    response = authenticate(client, body)
    assert response.status_code == 400

def test_invalid_username(client):
    path = "/account/test001"
    body = {
        "password": "Z00keeper!2#",
        "email": "worldskills.developer@gmail.com"
    }
    response = create_account(client, path, body)
    assert response.status_code == 201

    body = {
        "username": "nouser",
        "password": "Z00keeper!2#"
    }
    response = authenticate(client, body)
    assert response.status_code == 403

def test_invalid_password(client):
    path = "/account/test001"
    body = {
        "password": "Z00keeper!2#",
        "email": "worldskills.developer@gmail.com"
    }
    response = create_account(client, path, body)
    assert response.status_code == 201

    body = {
        "username": "test001",
        "password": "nopassword"
    }
    response = authenticate(client, body)
    assert response.status_code == 403