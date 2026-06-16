"""Offline-only safeguards for infrastructure adapters."""

from urllib.parse import urlparse


class OfflinePolicy:
    """Reject network endpoints so adapters cannot introduce cloud dependencies."""

    _blocked_schemes = {"http", "https", "ws", "wss", "ftp", "ftps"}

    def validate_resource_uri(self, uri: str) -> None:
        """Raise ValueError when a URI would require internet/network access."""

        parsed = urlparse(uri)
        if parsed.scheme.lower() in self._blocked_schemes:
            raise ValueError("UICMP is offline-only; network resources are not permitted.")
