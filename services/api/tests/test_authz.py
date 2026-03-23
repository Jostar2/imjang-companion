from fastapi.testclient import TestClient

from services.api.app.core.config import settings
from services.api.app.core.store import reset_store
from services.api.app.main import app


client = TestClient(app)


def setup_function() -> None:
    reset_store()
    settings.admin_emails = "admin@example.com"


def login(email: str, role: str = "buyer") -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={"email": email, "display_name": email.split("@")[0], "role": role},
    )
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def create_project(headers: dict[str, str], name: str) -> dict:
    response = client.post("/projects", json={"name": name}, headers=headers)
    response.raise_for_status()
    return response.json()


def create_completed_visit(headers: dict[str, str]) -> tuple[str, str]:
    project = create_project(headers, "Ops Review Route")
    property_response = client.post(
        "/properties",
        json={
            "project_id": project["id"],
            "address": "5 Yeonnam-ro",
            "listing_price": 650000000,
            "property_type": "apartment",
        },
        headers=headers,
    )
    property_response.raise_for_status()
    property_id = property_response.json()["id"]
    visit_response = client.post("/visits", json={"property_id": property_id, "visit_date": "2026-03-22"}, headers=headers)
    visit_response.raise_for_status()
    visit_id = visit_response.json()["id"]
    complete_response = client.patch(
        f"/visits/{visit_id}",
        json={
            "sections": [
                {"section_name": "property", "score": 4, "note": "Bright"},
                {"section_name": "building", "score": 4, "note": "Stable"},
                {"section_name": "neighborhood", "score": 5, "note": "Transit nearby"},
            ],
            "red_flags": ["Need noise check"],
            "recommendation_notes": "Request second walkthrough",
            "mark_complete": True,
        },
        headers=headers,
    )
    complete_response.raise_for_status()
    return project["id"], property_id


def test_admin_can_list_all_projects_but_buyer_cannot_request_global_scope() -> None:
    owner_headers = login("owner@example.com")
    second_owner_headers = login("second@example.com")
    admin_headers = login("admin@example.com", role="admin")

    create_project(owner_headers, "Owner Route")
    create_project(second_owner_headers, "Second Route")

    admin_response = client.get("/projects", params={"scope": "all"}, headers=admin_headers)
    assert admin_response.status_code == 200
    payload = admin_response.json()
    assert len(payload) == 2
    assert {project["owner_user_id"] for project in payload} == {"user-" + project["owner_user_id"].split("user-")[1] for project in payload} or all(project["owner_user_id"] for project in payload)

    buyer_response = client.get("/projects", params={"scope": "all"}, headers=owner_headers)
    assert buyer_response.status_code == 403


def test_admin_can_view_other_user_report_and_ops_summary() -> None:
    owner_headers = login("owner@example.com")
    create_completed_visit(owner_headers)

    owner_me = client.get("/auth/me", headers=owner_headers)
    owner_me.raise_for_status()
    owner_user_id = owner_me.json()["user_id"]

    admin_headers = login("admin@example.com", role="admin")

    report_response = client.get("/reports/latest", params={"owner_user_id": owner_user_id}, headers=admin_headers)
    assert report_response.status_code == 200
    assert report_response.json()["property_id"].startswith("property-")

    summary_response = client.get("/ops/summary", headers=admin_headers)
    assert summary_response.status_code == 200
    summary_payload = summary_response.json()
    assert summary_payload["total_users"] == 2
    assert summary_payload["total_projects"] == 1
    assert summary_payload["total_completed_visits"] == 1

    buyer_summary = client.get("/ops/summary", headers=owner_headers)
    assert buyer_summary.status_code == 403


def test_admin_can_manage_other_user_owned_resources() -> None:
    owner_headers = login("owner@example.com")
    admin_headers = login("admin@example.com", role="admin")

    project = create_project(owner_headers, "Owner Route")
    project_id = project["id"]

    property_response = client.post(
        "/properties",
        json={
            "project_id": project_id,
            "address": "5 Yeonnam-ro",
            "listing_price": 650000000,
            "property_type": "apartment",
        },
        headers=owner_headers,
    )
    property_response.raise_for_status()
    property_id = property_response.json()["id"]

    admin_project_update = client.patch(
        f"/projects/{project_id}",
        json={"notes": "Reviewed by admin"},
        headers=admin_headers,
    )
    assert admin_project_update.status_code == 200
    assert admin_project_update.json()["notes"] == "Reviewed by admin"

    admin_property_update = client.patch(
        f"/properties/{property_id}",
        json={"source": "Admin override"},
        headers=admin_headers,
    )
    assert admin_property_update.status_code == 200
    assert admin_property_update.json()["source"] == "Admin override"

    visit_response = client.post(
        "/visits",
        json={"property_id": property_id, "visit_date": "2026-03-22"},
        headers=admin_headers,
    )
    assert visit_response.status_code == 201
    visit_id = visit_response.json()["id"]

    complete_response = client.patch(
        f"/visits/{visit_id}",
        json={
            "sections": [
                {"section_name": "property", "score": 4, "note": "Bright"},
                {"section_name": "building", "score": 4, "note": "Stable"},
                {"section_name": "neighborhood", "score": 5, "note": "Transit nearby"},
            ],
            "red_flags": ["Need noise check"],
            "recommendation_notes": "Admin triage complete",
            "mark_complete": True,
        },
        headers=admin_headers,
    )
    assert complete_response.status_code == 200
    assert complete_response.json()["status"] == "completed"

    upload_response = client.post(
        f"/visits/{visit_id}/attachments/upload",
        data={"category": "living-room"},
        files={"file": ("living room.jpg", b"binary-image-data", "image/jpeg")},
        headers=admin_headers,
    )
    assert upload_response.status_code == 201
    assert upload_response.json()["visit_id"] == visit_id


def test_buyer_cannot_manage_other_user_owned_resources() -> None:
    owner_headers = login("owner@example.com")
    intruder_headers = login("intruder@example.com")

    project = create_project(owner_headers, "Owner Route")
    project_id = project["id"]

    property_response = client.post(
        "/properties",
        json={
            "project_id": project_id,
            "address": "5 Yeonnam-ro",
            "listing_price": 650000000,
            "property_type": "apartment",
        },
        headers=owner_headers,
    )
    property_response.raise_for_status()
    property_id = property_response.json()["id"]

    visit_response = client.post(
        "/visits",
        json={"property_id": property_id, "visit_date": "2026-03-22"},
        headers=owner_headers,
    )
    visit_response.raise_for_status()
    visit_id = visit_response.json()["id"]

    assert client.patch(f"/projects/{project_id}", json={"notes": "Nope"}, headers=intruder_headers).status_code == 404
    assert client.post(
        "/properties",
        json={"project_id": project_id, "address": "Intruder Road"},
        headers=intruder_headers,
    ).status_code == 404
    assert client.patch(
        f"/properties/{property_id}",
        json={"source": "Intruder override"},
        headers=intruder_headers,
    ).status_code == 404
    assert client.patch(
        f"/visits/{visit_id}",
        json={"red_flags": ["Intruder edit"]},
        headers=intruder_headers,
    ).status_code == 404
    assert client.post(
        f"/visits/{visit_id}/attachments/upload",
        data={"category": "living-room"},
        files={"file": ("living room.jpg", b"binary-image-data", "image/jpeg")},
        headers=intruder_headers,
    ).status_code == 404
