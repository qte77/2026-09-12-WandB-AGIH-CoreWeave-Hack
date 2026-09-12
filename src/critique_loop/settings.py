from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# pydantic-settings parses .env into this class's own fields only — it does NOT export
# them to os.environ. wandb/weave (and typesafe_sdk's own auto-detection) read
# WANDB_API_KEY/TYPESAFE_API_KEY etc. straight from the real environment, so load_dotenv()
# must run before anything else touches those libraries.
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Provider-agnostic on purpose (per rejected freellmapi — "personal experimentation
    # only" per its own README — OpenRouter is the actual decision, see findings.md):
    # any OpenAI-compatible endpoint works via base_url, no vendor lock-in.
    openrouter_api_key: str
    openrouter_model: str  # pick one at https://openrouter.ai/models, e.g. "anthropic/claude-sonnet-5"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # TypeSafe reads TYPESAFE_API_KEY itself (see triage.py) — kept here too so
    # get_settings() fails fast with a clear "missing" error if it's absent.
    typesafe_api_key: str

    wandb_api_key: str
    wandb_entity: str | None = None
    wandb_project: str = "coreweave-hacks-2026-09"

    max_refine_iterations: int = 3


def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
