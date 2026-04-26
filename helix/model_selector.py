"""Model selection logic based on hardware capabilities."""

from helix.hardware import HardwareProfile
from helix.config import config
import logging

logger = logging.getLogger(__name__)

class ModelSelector:
    """Selects the best models given the hardware profile."""

    def select(self, profile: HardwareProfile) -> None:
        """
        Updates the global config with selected models based on hardware tier.
        Tier 1: High VRAM (>=24GB)
        Tier 2: Med VRAM (>=10GB)
        Tier 3: Low VRAM (>=6GB)
        Tier 4: Minimal VRAM (<6GB)
        Tier 5: CPU only
        """
        tier = config.model.force_tier if config.model.force_tier is not None else profile.tier

        # Set text model
        if tier == 1:
            config.model.text_model = "llama3:70b"
        elif tier == 2:
            config.model.text_model = "llama3:8b"
        elif tier == 3:
            config.model.text_model = "mistral:7b"
        elif tier == 4:
            config.model.text_model = "phi3:mini"
        else:
            config.model.text_model = "gemma:2b" # CPU fallback

        # Set vision model
        if tier <= 2:
            config.model.vision_model = "llava:13b"
        elif tier <= 4:
            config.model.vision_model = "llava:7b"
        else:
            config.model.vision_model = "moondream:latest"

        # Set embed model (usually nomic-embed-text for all, since it's small)
        config.model.embed_model = "nomic-embed-text"

        # Set STT model
        if tier <= 2:
            config.model.stt_model = "large-v3"
        elif tier <= 4:
            config.model.stt_model = "small.en"
        else:
            config.model.stt_model = "tiny.en"

        logger.info(f"ModelSelector mapping for Tier {tier}: Text={config.model.text_model}, Vision={config.model.vision_model}, STT={config.model.stt_model}")
