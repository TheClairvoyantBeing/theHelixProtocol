# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""Configuration management for HELIX."""

import os
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

import tomllib

class VaultSettings(BaseModel):
    root_dirs: list[str] = ["~/Documents", "~/Pictures"]
    index_path: str = "~/.helix"
    watch_changes: bool = True
    open_browser: bool = True
    debug: bool = False

class ModelSettings(BaseModel):
    ollama_base: str = "http://localhost:11434"
    lm_studio_base: str = "http://localhost:1234"
    force_tier: int | None = None
    vision_model: str | None = None
    text_model: str | None = None
    embed_model: str | None = None
    stt_model: str | None = None

class ProcessingSettings(BaseModel):
    video_sample_interval: int = 30
    max_image_dim: int = 1024
    ocr_language: str = "eng"
    max_workers: int = 4
    max_file_size_mb: int = 500
    max_llm_input_chars: int = 32000
    chunk_size_tokens: int = 1000
    chunk_overlap_tokens: int = 100

class UISettings(BaseModel):
    theme: str = "dark"
    max_context_k: int = 8
    port: int = 7331

class VoiceSettings(BaseModel):
    enabled: bool = False
    wake_word: str = "hey helix"
    tts_enabled: bool = False
    tts_engine: str = "piper"

class SchedulerSettings(BaseModel):
    nightly_reflex_hour: int = 2
    nightly_consolidation_hour: int = 1
    reminder_poll_interval_seconds: int = 60

class ExportSettings(BaseModel):
    staging_dir: str = "~/.helix/exports"
    max_export_age_hours: int = 24

class VaultConfig(BaseSettings):
    vault: VaultSettings = Field(default_factory=VaultSettings)
    model: ModelSettings = Field(default_factory=ModelSettings)
    processing: ProcessingSettings = Field(default_factory=ProcessingSettings)
    ui: UISettings = Field(default_factory=UISettings)
    voice: VoiceSettings = Field(default_factory=VoiceSettings)
    scheduler: SchedulerSettings = Field(default_factory=SchedulerSettings)
    export: ExportSettings = Field(default_factory=ExportSettings)

    @classmethod
    def load(cls) -> "VaultConfig":
        """Loads configuration from the TOML file."""
        config_path_env = os.environ.get("HELIX_CONFIG_PATH")
        if config_path_env:
            config_path = Path(config_path_env).expanduser()
        else:
            config_path = Path("~/.helix/config.toml").expanduser()

        if config_path.exists():
            with open(config_path, "rb") as f:
                data = tomllib.load(f)
            return cls(**data)
        return cls()

config = VaultConfig.load()
