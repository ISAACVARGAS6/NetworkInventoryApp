from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    network: str = "192.168.1.0/24"

    discovery_timeout: int = 500

    port_timeout: float = 0.25

    discovery_workers: int = 50

    port_workers: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()