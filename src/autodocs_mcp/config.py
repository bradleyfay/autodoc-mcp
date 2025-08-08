"""Configuration management for AutoDocs MCP Server."""

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, validator

from .security import validate_pypi_url


class AutoDocsConfig(BaseModel):
    """Application configuration."""

    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".autodocs" / "cache")
    max_concurrent: int = Field(default=10)
    request_timeout: int = Field(default=30)
    log_level: str = Field(default="INFO")
    pypi_base_url: str = Field(default="https://pypi.org/pypi")

    # Version-based caching settings (for future use)
    max_cached_versions_per_package: int = Field(default=3)
    cache_cleanup_days: int = Field(default=90)

    # Context settings (for future use)
    max_dependency_context: int = Field(default=8)
    max_context_tokens: int = Field(default=30000)

    # Performance and rate limiting settings
    max_retry_attempts: int = Field(default=3)
    base_retry_delay: float = Field(default=1.0)
    max_retry_delay: float = Field(default=30.0)
    circuit_breaker_threshold: int = Field(default=5)
    circuit_breaker_timeout: float = Field(default=60.0)
    rate_limit_requests_per_minute: int = Field(default=60)
    max_documentation_size: int = Field(default=50000)  # Characters

    @validator("pypi_base_url")
    def validate_pypi_url_field(cls, v: str) -> str:
        """Validate PyPI URL using security module."""
        return validate_pypi_url(v)

    @classmethod
    def from_env(cls) -> "AutoDocsConfig":
        """Load configuration from environment variables."""
        cache_dir_str = os.getenv(
            "AUTODOCS_CACHE_DIR", str(Path.home() / ".autodocs" / "cache")
        )

        return cls(
            cache_dir=Path(cache_dir_str),
            max_concurrent=int(os.getenv("AUTODOCS_MAX_CONCURRENT", "10")),
            request_timeout=int(os.getenv("AUTODOCS_REQUEST_TIMEOUT", "30")),
            log_level=os.getenv("AUTODOCS_LOG_LEVEL", "INFO"),
            pypi_base_url=os.getenv("AUTODOCS_PYPI_URL", "https://pypi.org/pypi"),
            max_cached_versions_per_package=int(
                os.getenv("AUTODOCS_MAX_VERSIONS", "3")
            ),
            cache_cleanup_days=int(os.getenv("AUTODOCS_CLEANUP_DAYS", "90")),
            max_dependency_context=int(os.getenv("AUTODOCS_MAX_DEPS", "8")),
            max_context_tokens=int(os.getenv("AUTODOCS_MAX_TOKENS", "30000")),
            # ADD MISSING PARAMETERS:
            max_retry_attempts=int(os.getenv("AUTODOCS_MAX_RETRY_ATTEMPTS", "3")),
            base_retry_delay=float(os.getenv("AUTODOCS_BASE_RETRY_DELAY", "1.0")),
            max_retry_delay=float(os.getenv("AUTODOCS_MAX_RETRY_DELAY", "30.0")),
            circuit_breaker_threshold=int(
                os.getenv("AUTODOCS_CIRCUIT_BREAKER_THRESHOLD", "5")
            ),
            circuit_breaker_timeout=float(
                os.getenv("AUTODOCS_CIRCUIT_BREAKER_TIMEOUT", "60.0")
            ),
            rate_limit_requests_per_minute=int(
                os.getenv("AUTODOCS_RATE_LIMIT_RPM", "60")
            ),
            max_documentation_size=int(os.getenv("AUTODOCS_MAX_DOC_SIZE", "50000")),
        )

    def model_post_init(self, __context: Any) -> None:
        """Ensure cache directory exists."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_config() -> AutoDocsConfig:
    """Get cached configuration instance."""
    return AutoDocsConfig.from_env()
