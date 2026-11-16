import pytest
from app import create_app
from models import db

@pytest.fixture
def app(tmp_path):
    app = create_app({"TESTING": True, "SECRET_KEY": "test-only", "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(tmp_path / "isolated.db")})
    with app.app_context():
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    client = app.test_client()
    client.get("/contacts/new")
    return client

@pytest.fixture
def post(client):
    def submit(url, data=None, **kwargs):
        with client.session_transaction() as session:
            token = session["csrf_token"]
        return client.post(url, data={"csrf_token": token, **(data or {})}, **kwargs)
    return submit
