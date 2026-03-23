from __future__ import annotations

from collections.abc import Iterable

from services.api.app.core.db import ProjectRecord, PropertyRecord
from services.api.app.services.storage import storage_service


def iter_property_storage_keys(property_item: PropertyRecord) -> Iterable[str]:
    for visit in property_item.visits:
        for attachment in visit.attachments:
            if attachment.storage_key:
                yield attachment.storage_key


def iter_project_storage_keys(project: ProjectRecord) -> Iterable[str]:
    for property_item in project.properties:
        yield from iter_property_storage_keys(property_item)


def delete_property_storage(property_item: PropertyRecord) -> None:
    for storage_key in iter_property_storage_keys(property_item):
        storage_service.delete(storage_key)


def delete_project_storage(project: ProjectRecord) -> None:
    for storage_key in iter_project_storage_keys(project):
        storage_service.delete(storage_key)
