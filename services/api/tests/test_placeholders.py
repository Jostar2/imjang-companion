from fastapi.testclient import TestClient

from services.api.app.core.config import settings
from services.api.app.core.store import reset_store
from services.api.app.main import app


client = TestClient(app)


def auth_headers() -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={"email": "planner@example.com", "display_name": "Planner", "role": "buyer"},
    )
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def setup_function() -> None:
    reset_store()


def test_project_crud_flow() -> None:
    headers = auth_headers()
    response = client.post(
        "/projects",
        json={
            "name": "Seoul North Route",
            "region": "Mapo / Seogyo",
            "budget": "700M-900M KRW",
            "notes": "Weekend visit"
        },
        headers=headers,
    )

    assert response.status_code == 201
    project = response.json()
    assert project["name"] == "Seoul North Route"
    assert project["region"] == "Mapo / Seogyo"
    assert project["budget"] == "700M-900M KRW"

    list_response = client.get("/projects", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.patch(
        f"/projects/{project['id']}",
        json={"notes": "Updated route note", "budget": "680M-880M KRW"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["notes"] == "Updated route note"
    assert update_response.json()["budget"] == "680M-880M KRW"

    delete_response = client.delete(f"/projects/{project['id']}", headers=headers)
    assert delete_response.status_code == 204
    assert client.get("/projects", headers=headers).json() == []


def test_property_crud_flow() -> None:
    headers = auth_headers()
    project_response = client.post("/projects", json={"name": "Seoul North Route"}, headers=headers)
    project = project_response.json()

    response = client.post(
        "/properties",
        json={
            "project_id": project["id"],
            "address": "123 Sample Road",
            "listing_price": 500000000,
            "property_type": "apartment",
            "source": "Broker note"
        },
        headers=headers,
    )

    assert response.status_code == 201
    property_item = response.json()
    assert property_item["project_id"] == project["id"]
    assert property_item["source"] == "Broker note"

    list_response = client.get("/properties", params={"project_id": project["id"]}, headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.patch(
        f"/properties/{property_item['id']}",
        json={"listing_price": 530000000, "property_type": "officetel", "source": "Portal shortlist"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["listing_price"] == 530000000
    assert update_response.json()["source"] == "Portal shortlist"

    delete_response = client.delete(f"/properties/{property_item['id']}", headers=headers)
    assert delete_response.status_code == 204
    assert client.get("/properties", headers=headers).json() == []


def test_property_requires_existing_project() -> None:
    headers = auth_headers()
    response = client.post(
        "/properties",
        json={
            "project_id": "missing-project",
            "address": "123 Sample Road",
            "listing_price": 500000000,
            "property_type": "apartment",
        },
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_user_only_sees_owned_projects() -> None:
    owner_headers = auth_headers()
    other_headers = client.post(
        "/auth/login",
        json={"email": "other@example.com", "display_name": "Other User", "role": "buyer"},
    )
    other_token = other_headers.json()["token"]

    created = client.post("/projects", json={"name": "Owner Route"}, headers=owner_headers).json()

    assert client.get("/projects", headers=owner_headers).json()[0]["id"] == created["id"]
    assert client.get("/projects", headers={"Authorization": f"Bearer {other_token}"}).json() == []


def test_admin_can_access_release_readiness_endpoint() -> None:
    settings.admin_emails = "admin@example.com"
    response = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "display_name": "Admin", "role": "admin"},
    )
    token = response.json()["token"]

    readiness = client.get("/ops/release-readiness", headers={"Authorization": f"Bearer {token}"})

    assert readiness.status_code == 200
    assert "run_status" in readiness.json()


def test_buyer_cannot_access_release_readiness_endpoint() -> None:
    headers = auth_headers()

    readiness = client.get("/ops/release-readiness", headers=headers)

    assert readiness.status_code == 403


def test_non_allowlisted_user_cannot_self_assign_admin_role() -> None:
    settings.admin_emails = "admin@example.com"
    response = client.post(
        "/auth/login",
        json={"email": "buyer@example.com", "display_name": "Buyer", "role": "admin"},
    )

    assert response.status_code == 200
    assert response.json()["role"] == "buyer"
