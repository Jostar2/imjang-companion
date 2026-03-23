from fastapi.testclient import TestClient

from services.api.app.core.store import reset_store
from services.api.app.main import app


client = TestClient(app)


def auth_headers(email: str = "planner@example.com") -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={"email": email, "display_name": email.split("@")[0], "role": "buyer"},
    )
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def setup_function() -> None:
    reset_store()


def create_property(headers: dict[str, str]) -> str:
    project_response = client.post("/projects", json={"name": "Imjang Route"}, headers=headers)
    project_id = project_response.json()["id"]
    property_response = client.post(
        "/properties",
        json={
            "project_id": project_id,
            "address": "231 Donggyo-ro, Mapo-gu",
            "listing_price": 820000000,
            "property_type": "apartment",
        },
        headers=headers,
    )
    return property_response.json()["id"]


def test_visit_completion_requires_required_sections() -> None:
    headers = auth_headers()
    property_id = create_property(headers)
    visit_response = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=headers)
    visit_id = visit_response.json()["id"]

    incomplete_response = client.patch(
        f"/visits/{visit_id}",
        json={
            "sections": [
                {"section_name": "property", "score": 4, "note": "Good sunlight"}
            ],
            "mark_complete": True
        },
        headers=headers,
    )

    assert incomplete_response.status_code == 400
    assert "building" in incomplete_response.json()["detail"]
    assert "neighborhood" in incomplete_response.json()["detail"]


def test_visit_can_be_completed_with_scores_and_attachment_metadata() -> None:
    headers = auth_headers()
    property_id = create_property(headers)
    visit_response = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=headers)
    visit_id = visit_response.json()["id"]

    update_response = client.patch(
        f"/visits/{visit_id}",
        json={
            "sections": [
                {"section_name": "property", "score": 4, "note": "Living room was bright"},
                {"section_name": "building", "score": 3, "note": "Elevator felt dated"},
                {"section_name": "neighborhood", "score": 5, "note": "Station is five minutes away"}
            ],
            "red_flags": ["Visible wall crack in bedroom"],
            "recommendation_notes": "Worth a second visit if noise remains acceptable.",
            "attachments": [
                {
                    "filename": "living-room.jpg",
                    "content_type": "image/jpeg",
                    "category": "living-room"
                }
            ],
            "mark_complete": True
        },
        headers=headers,
    )

    assert update_response.status_code == 200
    payload = update_response.json()
    assert payload["status"] == "completed"
    assert payload["missing_sections"] == []
    assert payload["total_score"] == 4.0
    assert payload["attachments"][0]["filename"] == "living-room.jpg"
    assert payload["attachments"][0]["size_bytes"] == 0


def test_visit_list_filters_by_property() -> None:
    headers = auth_headers()
    property_id = create_property(headers)
    client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=headers)
    client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-23"}, headers=headers)

    list_response = client.get("/visits", params={"property_id": property_id}, headers=headers)

    assert list_response.status_code == 200
    assert len(list_response.json()) == 2


def test_visit_allows_clearing_red_flags() -> None:
    headers = auth_headers()
    property_id = create_property(headers)
    visit_response = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=headers)
    visit_id = visit_response.json()["id"]

    client.patch(
        f"/visits/{visit_id}",
        json={
            "sections": [
                {"section_name": "property", "score": 4, "note": "Good"},
                {"section_name": "building", "score": 4, "note": "Stable"},
                {"section_name": "neighborhood", "score": 4, "note": "Convenient"}
            ],
            "red_flags": ["Noise after 10pm"]
        },
        headers=headers,
    )

    clear_response = client.patch(f"/visits/{visit_id}", json={"red_flags": []}, headers=headers)

    assert clear_response.status_code == 200
    assert clear_response.json()["red_flags"] == []


def test_deleting_property_removes_associated_visits() -> None:
    headers = auth_headers()
    property_id = create_property(headers)
    visit_response = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=headers)
    visit_id = visit_response.json()["id"]

    delete_response = client.delete(f"/properties/{property_id}", headers=headers)

    assert delete_response.status_code == 204
    assert client.get(f"/visits/{visit_id}", headers=headers).status_code == 404


def test_binary_attachment_upload_links_file_to_visit() -> None:
    headers = auth_headers()
    property_id = create_property(headers)
    visit_response = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=headers)
    visit_id = visit_response.json()["id"]

    upload_response = client.post(
        f"/visits/{visit_id}/attachments/upload",
        data={"category": "living-room"},
        files={"file": ("living room.jpg", b"binary-image-data", "image/jpeg")},
        headers=headers,
    )

    assert upload_response.status_code == 201
    payload = upload_response.json()
    assert payload["visit_id"] == visit_id
    assert payload["filename"] == "living-room.jpg"
    assert payload["size_bytes"] == len(b"binary-image-data")
    assert payload["storage_key"].startswith("artifacts/uploads/")


def test_visit_is_scoped_to_owner() -> None:
    owner_headers = auth_headers()
    property_id = create_property(owner_headers)
    visit_response = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=owner_headers)
    visit_id = visit_response.json()["id"]

    other_headers = auth_headers("other@example.com")

    assert client.get(f"/visits/{visit_id}", headers=other_headers).status_code == 404


def test_report_endpoints_return_backend_payloads() -> None:
    headers = auth_headers()
    property_id = create_property(headers)
    visit_response = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=headers)
    visit_id = visit_response.json()["id"]

    client.patch(
        f"/visits/{visit_id}",
        json={
            "sections": [
                {"section_name": "property", "score": 4, "note": "Good"},
                {"section_name": "building", "score": 4, "note": "Stable"},
                {"section_name": "neighborhood", "score": 5, "note": "Convenient"}
            ],
            "red_flags": ["Noise after 10pm"],
            "recommendation_notes": "Worth a second visit.",
            "mark_complete": True
        },
        headers=headers,
    ).raise_for_status()

    comparison_response = client.get("/reports/comparison", headers=headers)
    report_response = client.get("/reports/latest", headers=headers)

    assert comparison_response.status_code == 200
    comparison_payload = comparison_response.json()
    assert comparison_payload["project_count"] == 1
    assert comparison_payload["entries"][0]["property_id"] == property_id

    assert report_response.status_code == 200
    report_payload = report_response.json()
    assert report_payload["property_id"] == property_id
    assert report_payload["sections"][0]["title"] == "Visit summary"
