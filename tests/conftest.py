import pytest
from webapp import create_app


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email="admin@example.com", password="password"):
        return self._client.post(
            "/auth/login", data=dict(email=email, password=password)
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'memory://',
        'result_backend': 'rpc'
    }
