"""
    account CRUD(생성/수정/삭제/업데이트) 중 Delete 작업이 정상적으로 수행되는 지 확인합니다.
"""
import json

def create_account(client, path, body):
    return client.post(
        path,
        data=json.dumps(body),
        content_type='application/json',
        follow_redirects=True 
    )

def delete_account(client, path):
    return client.delete(
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
    response = delete_account(client, path)
    assert response.status_code == 200

def test_content_not_found(client):
    path = "/account/test001"
    response = delete_account(client, path)
    assert response.status_code == 404