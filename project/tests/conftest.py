import os
from base64 import b64encode

import pytest
from app.config import Settings, get_settings
from app.main import create_application
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers_and_payload():
    def _auth_headers_and_payload(username, password):
        credentials = f"{username}:{password}"
        encoded_credentials = b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
        }

        payload = {"title": "Ашипка", "content": "Первый текст с ашипкой."}

        return headers, payload

    return _auth_headers_and_payload
