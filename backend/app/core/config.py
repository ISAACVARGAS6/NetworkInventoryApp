from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    network: str = "192.168.1.0/24"

    discovery_timeout: int = 500

    port_timeout: float = 0.25

    discovery_workers: int = 50

    port_workers: int = 30

    # A scan is intentionally constrained to the networks explicitly allowed
    # by the operator.  This prevents an API client from using the service as
    # an unrestricted network scanner.
    authorized_networks: str | None = None

    max_hosts_per_scan: int = 1024

    oui_file: str = str(
        Path(__file__).resolve().parents[2] / "oui.txt"
    )

    @field_validator("network")
    @classmethod
    def validate_network(cls, value: str) -> str:
        # Import lazily to keep settings import errors concise for the user.
        from ipaddress import IPv4Network, ip_network

        parsed = ip_network(value, strict=False)
        if not isinstance(parsed, IPv4Network):
            raise ValueError("NETWORK must be an IPv4 CIDR network")
        return str(parsed)

    @field_validator("authorized_networks")
    @classmethod
    def validate_authorized_networks(cls, value: str | None) -> str | None:
        if value is None or not value.strip():
            return None

        from ipaddress import IPv4Network, ip_network

        networks = []
        for item in value.split(","):
            parsed = ip_network(item.strip(), strict=False)
            if not isinstance(parsed, IPv4Network):
                raise ValueError("AUTHORIZED_NETWORKS must contain IPv4 CIDRs")
            networks.append(str(parsed))
        return ",".join(networks)

    @field_validator("max_hosts_per_scan")
    @classmethod
    def validate_max_hosts(cls, value: int) -> int:
        if value < 1:
            raise ValueError("MAX_HOSTS_PER_SCAN must be at least 1")
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
