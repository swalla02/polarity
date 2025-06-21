from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_comments_polarity_limit_success():
    response = client.post("/api/v1/comments_polarity/limit", json={
        "feddit_name": "Dummy Topic 1",
        "limit": 5
    })
    assert response.status_code == 200
    assert "comments" in response.json()

def test_comments_polarity_limit_missing_name():
    response = client.post("/api/v1/comments_polarity/limit", json={
        "limit": 5
    })
    assert response.status_code != 200
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_comments_polarity_with_time_success():
    response = client.post("/api/v1/comments_polarity/with_time", json={
        "feddit_name": "Dummy Topic 1",
        "time_range": ["2021-08-16T00:00:00", "2021-08-19T23:59:59"]
    })
    assert response.status_code == 200
    assert "comments_with_time" in response.json()
