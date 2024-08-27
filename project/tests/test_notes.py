import json

import pytest


def test_create_note_with_corrected_spelling(test_app_with_db):
    headers = {
        "username": "user1",
        "password": "password1",
        "Content-Type": "application/json"
    }

    payload = {
        "title": "Ашипка",
        "content": "Первый текст с ашипкой."
    }

    response = test_app_with_db.post("/notes/", headers=headers,
                                     data=json.dumps(payload))

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["title"] == "Ошибка"
    assert response_data["content"] == "Первый текст с ошибкой."


def test_create_note_with_wrong_password(test_app_with_db):
    headers = {
        "username": "user1",
        "password": "wrong",
        "Content-Type": "application/json"
    }

    payload = {
        "title": "Ашипка",
        "content": "Первый текст с ашипкой."
    }
    response = test_app_with_db.post("/notes/", headers=headers,
                                     data=json.dumps(payload))
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_create_notes_invalid_json(test_app):
    response = test_app.post("/notes/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["header", "username"],
                "msg": "Field required",
                "input": None,
                "url": "https://errors.pydantic.dev/2.8/v/missing"
            },
            {
                "type": "missing",
                "loc": ["header", "password"],
                "msg": "Field required",
                "input": None,
                "url": "https://errors.pydantic.dev/2.8/v/missing"
            },
            {
                "type": "missing",
                "loc": ["body", "title"],
                "msg": "Field required",
                "input": {},
                "url": "https://errors.pydantic.dev/2.8/v/missing"
            },
            {
                "type": "missing",
                "loc": ["body", "content"],
                "msg": "Field required",
                "input": {},
                "url": "https://errors.pydantic.dev/2.8/v/missing"
            }
        ]
    }


@pytest.mark.parametrize("headers, payload, expected_user", [
    (
        {"username": "user1", "password": "password1", "Content-Type": "application/json"},
        {"title": "Test Note", "content": "This is a note for user1."},
        "user1"
    ),
    (
        {"username": "user2", "password": "password2", "Content-Type": "application/json"},
        {"title": "Test Note", "content": "This is a note for user2."},
        "user2"
    )
])
def test_read_all_notes_and_check_for_correct_user(test_app_with_db, headers, payload, expected_user):
    # Create a note
    response = test_app_with_db.post("/notes/", headers=headers, data=json.dumps(payload))
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
