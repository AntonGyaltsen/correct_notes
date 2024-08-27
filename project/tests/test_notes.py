import json
from base64 import b64encode

import pytest


@pytest.mark.parametrize(
    "username, password, expected_title, expected_content",
    [
        ("user1", "password1", "Ошибка", "Первый текст с ошибкой."),
        ("user2", "password2", "Ошибка", "Первый текст с ошибкой."),
    ],
)
def test_create_note_with_corrected_spelling(
    test_app_with_db,
    auth_headers_and_payload,
    username,
    password,
    expected_title,
    expected_content,
):
    headers, payload = auth_headers_and_payload(username, password)

    response = test_app_with_db.post(
        "/notes/", headers=headers, data=json.dumps(payload)
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["title"] == expected_title
    assert response_data["content"] == expected_content


def test_create_note_with_wrong_password(test_app_with_db):
    username = "user1"
    password = "wrong"
    credentials = f"{username}:{password}"
    encoded_credentials = b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json",
    }

    payload = {"title": "Ашипка", "content": "Первый текст с ашипкой."}
    response = test_app_with_db.post(
        "/notes/", headers=headers, data=json.dumps(payload)
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_create_notes_invalid_json(test_app):
    username = "user1"
    password = "password1"
    credentials = f"{username}:{password}"
    encoded_credentials = b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json",
    }

    response = test_app.post("/notes/", headers=headers, data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "title"],
                "msg": "Field required",
                "input": {},
                "url": "https://errors.pydantic.dev/2.8/v/missing",
            },
            {
                "type": "missing",
                "loc": ["body", "content"],
                "msg": "Field required",
                "input": {},
                "url": "https://errors.pydantic.dev/2.8/v/missing",
            },
        ]
    }

    # Test without the Authorization header
    response = test_app.post("/notes/", data=json.dumps({}))
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize(
    "username, password, payload, expected_user",
    [
        (
            "user1",
            "password1",
            {"title": "Test Note", "content": "This is a note for user1."},
            "user1",
        ),
        (
            "user2",
            "password2",
            {"title": "Test Note", "content": "This is a note for user2."},
            "user2",
        ),
    ],
)
def test_read_all_notes_and_check_for_correct_user(
    test_app_with_db, username, password, payload, expected_user
):
    # Encode the credentials in Base64
    credentials = f"{username}:{password}"
    encoded_credentials = b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json",
    }

    # Create a note
    response = test_app_with_db.post(
        "/notes/", headers=headers, data=json.dumps(payload)
    )
    assert response.status_code == 201
    note_id = response.json()["id"]

    # Fetch all notes for the given user
    response = test_app_with_db.get("/notes/", headers=headers)
    assert response.status_code == 200

    response_list = response.json()

    # Check that all notes belong to the expected user
    assert all(note["user"] == expected_user for note in response_list)
    # Check that the created note is in the list
    assert any(note["id"] == note_id for note in response_list)
