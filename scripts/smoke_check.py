from __future__ import annotations

import argparse
import sys

import httpx


def main() -> int:
    parser = argparse.ArgumentParser(description="Run core API smoke checks against a deployed environment.")
    parser.add_argument("--base-url", required=True, help="Base API URL, for example http://localhost:8000")
    parser.add_argument(
        "--include-attachment",
        action="store_true",
        help="Also verify the attachment upload path during smoke checks.",
    )
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    with httpx.Client(base_url=base_url, timeout=10.0) as client:
        health = client.get("/health")
        health.raise_for_status()

        session_response = client.post(
            "/auth/login",
            json={
                "email": "smoke-runner@example.com",
                "display_name": "Smoke Runner",
                "role": "buyer",
            },
        )
        session_response.raise_for_status()
        token = session_response.json()["token"]
        auth_headers = {"Authorization": f"Bearer {token}"}

        project = (
            client.post("/projects", json={"name": "Smoke Route", "notes": "staging smoke"}, headers=auth_headers)
            .raise_for_status()
            .json()
        )
        property_item = (
            client.post(
                "/properties",
                json={
                    "project_id": project["id"],
                    "address": "100 Smoke Street",
                    "listing_price": 500000000,
                    "property_type": "apartment",
                },
                headers=auth_headers,
            )
            .raise_for_status()
            .json()
        )
        visit = (
            client.post(
                "/visits",
                json={"property_id": property_item["id"], "visit_date": "2026-03-22"},
                headers=auth_headers,
            )
            .raise_for_status()
            .json()
        )
        completed = (
            client.patch(
                f"/visits/{visit['id']}",
                json={
                    "sections": [
                        {"section_name": "property", "score": 4, "note": "Good layout"},
                        {"section_name": "building", "score": 3, "note": "Acceptable building condition"},
                        {"section_name": "neighborhood", "score": 5, "note": "Strong transit access"},
                    ],
                    "red_flags": ["Street noise should be rechecked"],
                    "recommendation_notes": "Worth a second visit.",
                    "mark_complete": True,
                },
                headers=auth_headers,
            )
            .raise_for_status()
            .json()
        )

        if completed["status"] != "completed":
            raise RuntimeError("Visit did not reach completed status during smoke check")

        if args.include_attachment:
            files = {"file": ("smoke-proof.jpg", b"smoke-binary-data", "image/jpeg")}
            data = {"category": "smoke-proof"}
            upload = client.post(
                f"/visits/{visit['id']}/attachments/upload",
                data=data,
                files=files,
                headers=auth_headers,
            )
            upload.raise_for_status()
            payload = upload.json()
            if payload["size_bytes"] != len(b"smoke-binary-data"):
                raise RuntimeError("Attachment size did not match uploaded payload")

    print("smoke-ok")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"smoke-failed: {error}")
        raise
