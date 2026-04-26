from helix.config import VaultConfig
from pydantic_settings import BaseSettings

def test_config_load():
    config = VaultConfig.load()
    assert config.vault.index_path == "~/.helix"
    assert config.ui.port == 7331
    assert config.voice.wake_word == "hey helix"
