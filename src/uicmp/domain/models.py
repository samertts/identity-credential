"""Domain models shared across application services.

The project standardizes on Pydantic for production validation; this baseline keeps
framework-independent model semantics in the domain layer so UI and persistence
concerns cannot leak into business rules.
"""

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from uicmp.domain.enums import CredentialState, TemplateStatus


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""

    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class VersionedModel:
    """Base for all versioned, non-physically-deleted domain records."""

    id: UUID = field(default_factory=uuid4)
    version: int = 1
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    archived_at: datetime | None = None

    def __post_init__(self) -> None:
        if self.version < 1:
            raise ValueError("version must be greater than or equal to 1")

    @property
    def is_archived(self) -> bool:
        """Soft-delete/archival marker used instead of physical deletion."""

        return self.archived_at is not None

    def model_copy(self, *, update: dict[str, Any] | None = None) -> "VersionedModel":
        """Compatibility helper matching the Pydantic model_copy API used by services."""

        return replace(self, **(update or {}))


@dataclass(frozen=True, slots=True)
class Entity(VersionedModel):
    """Universal party record for people, organizations, and departments."""

    entity_type: str = "person"
    display_name: str = ""
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class TemplateVersion(VersionedModel):
    """Certified template definition for one immutable template revision."""

    template_id: UUID = field(default_factory=uuid4)
    status: TemplateStatus = TemplateStatus.DRAFT
    layout: dict[str, Any] = field(default_factory=dict)
    certification_hash: str | None = None

    @property
    def is_certified(self) -> bool:
        """Whether this template version can be used for production credentials."""

        return self.status in {TemplateStatus.CERTIFIED, TemplateStatus.PUBLISHED} and bool(
            self.certification_hash
        )


@dataclass(frozen=True, slots=True)
class Credential(VersionedModel):
    """Credential aggregate root with lifecycle state and audit-friendly metadata."""

    entity_id: UUID = field(default_factory=uuid4)
    credential_type: str = "generic"
    state: CredentialState = CredentialState.DRAFT
    template_version_id: UUID | None = None
    approved_by: UUID | None = None
    printed_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
