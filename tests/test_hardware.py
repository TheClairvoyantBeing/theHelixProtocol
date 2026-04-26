from helix.hardware import HardwareProbe, HardwareProfile

def test_hardware_tier():
    probe = HardwareProbe()
    # Test fallback determination manually
    profile = HardwareProfile(gpu_vendor="nvidia", vram_gb=24.0)
    assert probe._determine_tier(profile) == 1

    profile = HardwareProfile(gpu_vendor="nvidia", vram_gb=10.0)
    assert probe._determine_tier(profile) == 2

    profile = HardwareProfile(gpu_vendor="nvidia", vram_gb=6.0)
    assert probe._determine_tier(profile) == 3

    profile = HardwareProfile(gpu_vendor="nvidia", vram_gb=4.0)
    assert probe._determine_tier(profile) == 4

    profile = HardwareProfile(gpu_vendor="amd", vram_gb=16.0)
    assert probe._determine_tier(profile) == 5

def test_probe_run():
    probe = HardwareProbe()
    profile = probe.run()
    assert profile.tier in [1, 2, 3, 4, 5]
    assert profile.cpu_cores > 0
