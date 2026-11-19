import pytest

from app import app, reset_tickets


@pytest.fixture
def client():
    reset_tickets()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list_tickets_returns_200(client):
    response = client.get("/api/tickets")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_get_ticket_1_has_a_title(client):
    response = client.get("/api/tickets/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Laptop not charging"


def test_unknown_ticket_returns_404(client):
    response = client.get("/api/tickets/9999")
    assert response.status_code == 404


def test_tickets_are_sorted_by_priority(client):
    response = client.get("/api/tickets")
    tickets = response.get_json()

    assert [ticket["priority"] for ticket in tickets] == [
        "High", "High", "Medium", "Medium", "Low"
    ]


def test_empty_title_returns_400(client):
    response = client.post("/api/tickets", json={"title": "   "})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Title is required"}


def test_resolved_ticket_screen_label(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert "<td>Resolved</td>" not in html
    assert "<span class=\"badge\">Resolved</span>" in html


def test_missing_title_returns_400(client):
    response = client.post("/api/tickets", json={"category": "Hardware"})
    assert response.status_code == 400


def test_unknown_category_returns_400(client):
    response = client.post(
        "/api/tickets",
        json={"title": "Printer jam", "category": "Furniture"},
    )
    assert response.status_code == 400


def test_unknown_priority_returns_400(client):
    response = client.post(
        "/api/tickets",
        json={"title": "Printer jam", "priority": "Urgent"},
    )
    assert response.status_code == 400


def test_unknown_status_returns_400(client):
    response = client.patch("/api/tickets/1/status", json={"status": "Unknown"})
    assert response.status_code == 400


def test_missing_status_returns_400(client):
    response = client.patch("/api/tickets/1/status", json={})
    assert response.status_code == 400


def test_status_change_for_unknown_ticket_returns_404(client):
    response = client.patch("/api/tickets/9999/status", json={"status": "Closed"})
    assert response.status_code == 404


def test_non_string_title_returns_400(client):
    response = client.post("/api/tickets", json={"title": 123})
    assert response.status_code == 400


def test_empty_request_body_returns_400(client):
    response = client.post("/api/tickets", data="", content_type="application/json")
    assert response.status_code == 400
