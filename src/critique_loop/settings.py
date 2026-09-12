from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str
    anthropic_model: str = "claude-sonnet-5"

    wandb_api_key: str
    wandb_entity: str | None = None
    wandb_project: str = "coreweave-hacks-2026-09"

    max_refine_iterations: int = 3


def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
