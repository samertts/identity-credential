"""Domain enumerations for identity and credential lifecycle management."""

from enum import StrEnum


class CredentialState(StrEnum):
    """Allowed states for the credential lifecycle."""

    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    GENERATED = "generated"
    PRINTED = "printed"
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    ARCHIVED = "archived"


class RoleName(StrEnum):
    """Built-in role names required by the RBAC baseline."""

    OPERATOR = "operator"
    REVIEWER = "reviewer"
    APPROVER = "approver"
    PRINTER = "printer"
    ADMINISTRATOR = "administrator"


class TemplateStatus(StrEnum):
    """Template publication and certification states."""

    DRAFT = "draft"
    VALIDATED = "validated"
    CERTIFIED = "certified"
    PUBLISHED = "published"
    ARCHIVED = "archived"
