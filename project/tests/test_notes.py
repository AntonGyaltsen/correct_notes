import json


def test_create_note(test_app_with_db):
    response = test_app_with_db.post("/notes/",
                                     data=json.dumps({"url": "https://foo.bar"}))

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_create_notes_invalid_json(test_app):
    response = test_app.post("/notes/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "url"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.8/v/missing",
            }
        ]
    }


def test_read_all_notes(test_app_with_db):
    response = test_app_with_db.post("/notes/",
                                     data=json.dumps({"url": "https://foo.bar"}))
    note_id = response.json()["id"]

    response = test_app_with_db.get("/notes/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == note_id, response_list))) == 1
