from helix.model_selector import ModelSelector
from helix.hardware import HardwareProfile
from helix.config import config

def test_model_selector_tier_2(mock_hardware_tier2):
    selector = ModelSelector()
    selector.select(mock_hardware_tier2)
    assert config.model.text_model == "llama3:8b"
    assert config.model.vision_model == "llava:13b"
    assert config.model.stt_model == "large-v3"
