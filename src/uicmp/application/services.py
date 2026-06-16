"""Application-layer services for enforcing cross-cutting platform invariants."""

from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID

from uicmp.domain.enums import CredentialState
from uicmp.domain.models import Credential, TemplateVersion, utc_now


class AuditSink(Protocol):
    """Port used by application services to write audit records."""

    def record(self, event_type: str, actor_id: UUID, payload: dict[str, str]) -> None:
        """Persist an append-only audit event."""


@dataclass(slots=True)
class InMemoryAuditSink:
    """Small test/demonstration audit sink; production adapters live in infrastructure."""

    events: list[tuple[str, UUID, dict[str, str]]] = field(default_factory=list)

    def record(self, event_type: str, actor_id: UUID, payload: dict[str, str]) -> None:
        self.events.append((event_type, actor_id, payload))


class CredentialLifecycleService:
    """Enforces credential lifecycle transitions and certification requirements."""

    _allowed_transitions = {
        CredentialState.DRAFT: {CredentialState.REVIEW, CredentialState.ARCHIVED},
        CredentialState.REVIEW: {CredentialState.APPROVED, CredentialState.DRAFT, CredentialState.ARCHIVED},
        CredentialState.APPROVED: {CredentialState.GENERATED, CredentialState.REVOKED, CredentialState.ARCHIVED},
        CredentialState.GENERATED: {CredentialState.PRINTED, CredentialState.REVOKED, CredentialState.ARCHIVED},
        CredentialState.PRINTED: {CredentialState.ACTIVE, CredentialState.REVOKED, CredentialState.ARCHIVED},
        CredentialState.ACTIVE: {CredentialState.EXPIRED, CredentialState.REVOKED, CredentialState.ARCHIVED},
        CredentialState.EXPIRED: {CredentialState.ARCHIVED},
        CredentialState.REVOKED: {CredentialState.ARCHIVED},
        CredentialState.ARCHIVED: set(),
    }

    def __init__(self, audit_sink: AuditSink) -> None:
        self._audit_sink = audit_sink

    def transition(
        self,
        credential: Credential,
        target_state: CredentialState,
        actor_id: UUID,
        *,
        template_version: TemplateVersion | None = None,
    ) -> Credential:
        """Return a new credential version after validating the requested transition."""

        allowed_targets = self._allowed_transitions[credential.state]
        if target_state not in allowed_targets:
            msg = f"Cannot transition credential from {credential.state} to {target_state}."
            raise ValueError(msg)

        if target_state is CredentialState.GENERATED:
            if template_version is None or not template_version.is_certified:
                raise ValueError("Credential generation requires a certified template version.")

        updated = credential.model_copy(
            update={
                "state": target_state,
                "version": credential.version + 1,
                "updated_at": utc_now(),
                "template_version_id": template_version.id if template_version else credential.template_version_id,
                "printed_at": utc_now() if target_state is CredentialState.PRINTED else credential.printed_at,
            }
        )
        self._audit_sink.record(
            "credential_state_changed",
            actor_id,
            {
                "credential_id": str(credential.id),
                "from": credential.state.value,
                "to": target_state.value,
            },
        )
        return updated
