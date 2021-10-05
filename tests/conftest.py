"""
    pytest의 fixture 데코레이터는 모든 테스트케이스 함수(test로 시작하는 함수)에 Argument로 사용할 수 있습니다.
    결과적으로 모든 테스트케이스에서 사용되는 로직 및 데이터를 한 곳에 작성함으로써 중복되는 코드를 줄일 수 있습니다.
    conftest.py 파일에 작성하면 모든 테스트 파일에서 사용할 수 있습니다.
"""

# Standard library
import os
import tempfile
# Third-party library
import pytest
# Application module
from app import create_app
from app import db

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    
    os.close(db_fd)
    os.unlink(db_path)
