from fastapi.testclient import TestClient

from services.api.app.core.store import reset_store
from services.api.app.main import app
from services.api.app.services.resource_cleanup import storage_service


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


def create_project(headers: dict[str, str], name: str = "Imjang Route") -> str:
    project_response = client.post("/projects", json={"name": name}, headers=headers)
    project_id = project_response.json()["id"]
    return project_id


def create_property(headers: dict[str, str], project_id: str | None = None, address: str = "231 Donggyo-ro, Mapo-gu") -> str:
    if project_id is None:
        project_id = create_project(headers)
    property_response = client.post(
        "/properties",
        json={
            "project_id": project_id,
            "address": address,
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


def test_deleting_property_removes_uploaded_binaries_from_storage(monkeypatch) -> None:
    deleted_keys: list[str] = []
    monkeypatch.setattr(storage_service, "delete", lambda storage_key: deleted_keys.append(storage_key))

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
    storage_key = upload_response.json()["storage_key"]

    delete_response = client.delete(f"/properties/{property_id}", headers=headers)

    assert delete_response.status_code == 204
    assert deleted_keys == [storage_key]


def test_deleting_project_removes_uploaded_binaries_from_storage(monkeypatch) -> None:
    deleted_keys: list[str] = []
    monkeypatch.setattr(storage_service, "delete", lambda storage_key: deleted_keys.append(storage_key))

    headers = auth_headers()
    project_id = create_project(headers)
    property_id = create_property(headers, project_id=project_id)
    visit_response = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=headers)
    visit_id = visit_response.json()["id"]

    upload_response = client.post(
        f"/visits/{visit_id}/attachments/upload",
        data={"category": "living-room"},
        files={"file": ("living room.jpg", b"binary-image-data", "image/jpeg")},
        headers=headers,
    )
    storage_key = upload_response.json()["storage_key"]

    delete_response = client.delete(f"/projects/{project_id}", headers=headers)

    assert delete_response.status_code == 204
    assert deleted_keys == [storage_key]


def test_visit_is_scoped_to_owner() -> None:
    owner_headers = auth_headers()
    property_id = create_property(owner_headers)
    visit_response = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=owner_headers)
    visit_id = visit_response.json()["id"]

    other_headers = auth_headers("other@example.com")

    assert client.get(f"/visits/{visit_id}", headers=other_headers).status_code == 404


def test_report_endpoints_return_backend_payloads() -> None:
    headers = auth_headers()
    project_id = create_project(headers)
    property_id = create_property(headers, project_id=project_id)
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

    comparison_response = client.get("/reports/comparison", params={"project_id": project_id}, headers=headers)
    report_response = client.get("/reports/latest", params={"project_id": project_id}, headers=headers)

    assert comparison_response.status_code == 200
    comparison_payload = comparison_response.json()
    assert comparison_payload["project_count"] == 1
    assert comparison_payload["project_id"] == project_id
    assert comparison_payload["property_count"] == 1
    assert comparison_payload["entries"][0]["property_id"] == property_id
    assert comparison_payload["entries"][0]["visit_id"] == visit_id

    assert report_response.status_code == 200
    report_payload = report_response.json()
    assert report_payload["project_id"] == project_id
    assert report_payload["visit_id"] == visit_id
    assert report_payload["property_id"] == property_id
    assert report_payload["sections"][0]["title"] == "Visit summary"


def test_report_endpoints_require_project_scope_when_multiple_projects_exist() -> None:
    headers = auth_headers()
    first_project_id = create_project(headers, name="Mapo shortlist")
    second_project_id = create_project(headers, name="Seongsu shortlist")
    first_property_id = create_property(headers, project_id=first_project_id, address="231 Donggyo-ro, Mapo-gu")
    second_property_id = create_property(headers, project_id=second_project_id, address="88 Seongsui-ro, Seongdong-gu")

    first_visit = client.post("/visits", json={"property_id": first_property_id, "visit_date": "2026-03-22"}, headers=headers).json()
    second_visit = client.post("/visits", json={"property_id": second_property_id, "visit_date": "2026-03-23"}, headers=headers).json()

    for visit_id, note in ((first_visit["id"], "Mapo follow-up"), (second_visit["id"], "Seongsu follow-up")):
        client.patch(
            f"/visits/{visit_id}",
            json={
                "sections": [
                    {"section_name": "property", "score": 4, "note": "Bright"},
                    {"section_name": "building", "score": 4, "note": "Stable"},
                    {"section_name": "neighborhood", "score": 5, "note": note},
                ],
                "mark_complete": True,
            },
            headers=headers,
        ).raise_for_status()

    missing_scope_comparison = client.get("/reports/comparison", headers=headers)
    missing_scope_report = client.get("/reports/latest", headers=headers)
    scoped_comparison = client.get("/reports/comparison", params={"project_id": second_project_id}, headers=headers)
    scoped_report = client.get("/reports/latest", params={"project_id": first_project_id}, headers=headers)

    assert missing_scope_comparison.status_code == 400
    assert "project_id is required" in missing_scope_comparison.json()["detail"]
    assert missing_scope_report.status_code == 400
    assert "project_id is required" in missing_scope_report.json()["detail"]
    assert scoped_comparison.status_code == 200
    assert scoped_comparison.json()["project_id"] == second_project_id
    assert [entry["property_id"] for entry in scoped_comparison.json()["entries"]] == [second_property_id]
    assert scoped_report.status_code == 200
    assert scoped_report.json()["project_id"] == first_project_id


def test_latest_report_can_target_a_completed_visit_directly() -> None:
    headers = auth_headers()
    project_id = create_project(headers)
    property_id = create_property(headers, project_id=project_id)
    first_visit = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=headers).json()
    second_visit = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-25"}, headers=headers).json()

    client.patch(
        f"/visits/{first_visit['id']}",
        json={
            "sections": [
                {"section_name": "property", "score": 4, "note": "First pass"},
                {"section_name": "building", "score": 3, "note": "Needs work"},
                {"section_name": "neighborhood", "score": 4, "note": "Transit okay"},
            ],
            "red_flags": ["Older boiler"],
            "recommendation_notes": "Only if price drops",
            "mark_complete": True,
        },
        headers=headers,
    ).raise_for_status()

    client.patch(
        f"/visits/{second_visit['id']}",
        json={
            "sections": [
                {"section_name": "property", "score": 5, "note": "Second pass"},
                {"section_name": "building", "score": 5, "note": "Better than expected"},
                {"section_name": "neighborhood", "score": 5, "note": "Transit excellent"},
            ],
            "red_flags": ["Weekend noise check pending"],
            "recommendation_notes": "Strong candidate",
            "mark_complete": True,
        },
        headers=headers,
    ).raise_for_status()

    report_response = client.get(
        "/reports/latest",
        params={"visit_id": first_visit["id"]},
        headers=headers,
    )

    assert report_response.status_code == 200
    assert report_response.json()["visit_id"] == first_visit["id"]
    assert report_response.json()["visit_date"] == "2026-03-22"
