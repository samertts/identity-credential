from uuid import uuid4

import pytest

from uicmp.application.services import CredentialLifecycleService, InMemoryAuditSink
from uicmp.domain.enums import CredentialState, TemplateStatus
from uicmp.domain.models import Credential, TemplateVersion


def test_generation_requires_certified_template() -> None:
    actor_id = uuid4()
    service = CredentialLifecycleService(InMemoryAuditSink())
    credential = Credential(entity_id=uuid4(), credential_type="employee", state=CredentialState.APPROVED)
    template = TemplateVersion(template_id=uuid4(), status=TemplateStatus.VALIDATED)

    with pytest.raises(ValueError, match="certified template"):
        service.transition(
            credential,
            CredentialState.GENERATED,
            actor_id,
            template_version=template,
        )


def test_valid_transition_versions_and_audits() -> None:
    actor_id = uuid4()
    audit = InMemoryAuditSink()
    service = CredentialLifecycleService(audit)
    credential = Credential(entity_id=uuid4(), credential_type="employee", state=CredentialState.APPROVED)
    template = TemplateVersion(
        template_id=uuid4(),
        status=TemplateStatus.CERTIFIED,
        certification_hash="sha256:abc",
    )

    updated = service.transition(
        credential,
        CredentialState.GENERATED,
        actor_id,
        template_version=template,
    )

    assert updated.state is CredentialState.GENERATED
    assert updated.version == credential.version + 1
    assert updated.template_version_id == template.id
    assert audit.events[0][0] == "credential_state_changed"


def test_invalid_transition_is_rejected() -> None:
    service = CredentialLifecycleService(InMemoryAuditSink())
    credential = Credential(entity_id=uuid4(), credential_type="visitor", state=CredentialState.DRAFT)

    with pytest.raises(ValueError, match="Cannot transition"):
        service.transition(credential, CredentialState.ACTIVE, uuid4())
