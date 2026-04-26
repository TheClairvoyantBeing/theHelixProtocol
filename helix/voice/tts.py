"""TTS module for reading responses aloud."""

import logging
from helix.config import config

logger = logging.getLogger(__name__)

class TTS:
    """Text-to-speech manager."""

    def __init__(self) -> None:
        self.enabled = config.voice.tts_enabled

    def speak(self, text: str) -> None:
        if not self.enabled:
            return
        logger.info(f"Speaking: {text}")
