import pytest

from uicmp.infrastructure.offline import OfflinePolicy


def test_offline_policy_rejects_network_resources() -> None:
    with pytest.raises(ValueError, match="offline-only"):
        OfflinePolicy().validate_resource_uri("https://example.com/template.png")


def test_offline_policy_allows_local_paths() -> None:
    OfflinePolicy().validate_resource_uri("file:///C:/uicmp/assets/logo.png")
    OfflinePolicy().validate_resource_uri("./assets/logo.png")
