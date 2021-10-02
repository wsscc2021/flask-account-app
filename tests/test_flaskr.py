# Standard library
import os
import tempfile
import json
# Third-party library
import pytest
# Application module
from app import create_app
from app.models import db

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite://{db_path}"
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    
    os.close(db_fd)
    os.unlink(db_path)


def create_user(client,username,password,email):
    return client.post(
        f'/account/{username}',
        data=json.dumps({
            "password": password,
            "email": email
        }),
        content_type='application/json',
        follow_redirects=True 
    )

def test_register(client):
    username = "user002"
    password = "P@sswoRd098"
    email = "worldskills.developer@gmail.com"

    rv = create_user(client, username, password, email)
    print(rv.data)
    assert rv.status_code == 201