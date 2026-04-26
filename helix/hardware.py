# Copyright (c) 2026 HELIX. All rights reserved.
# HELIX Personal Intelligence OS
"""Hardware detection and profiling module."""

import subprocess
import os
import platform
from dataclasses import dataclass

@dataclass
class HardwareProfile:
    """Represents the hardware capabilities of the host system."""
    gpu_name: str | None = None
    gpu_vendor: str | None = None
    vram_gb: float | None = None
    cuda_version: str | None = None
    cpu_cores: int = 0
    cpu_arch: str = ""
    ram_gb: float = 0.0
    platform: str = ""
    tier: int = 5  # Default to lowest tier


class HardwareProbe:
    """Probes the system for hardware capabilities."""

    def __init__(self) -> None:
        pass

    def run(self) -> HardwareProfile:
        """Runs the probe and returns a HardwareProfile."""
        profile = HardwareProfile()

        # CPU
        profile.cpu_cores = os.cpu_count() or 1
        profile.cpu_arch = platform.machine()
        profile.platform = platform.system().lower()

        # Basic RAM (approximate, if we really need it we can parse /proc/meminfo or use psutil)
        # For this tiering we just use GPU/CPU to decide for now

        # GPU Check (NVIDIA)
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False
            )
            if result.returncode == 0 and result.stdout:
                lines = result.stdout.strip().split("\n")
                if lines:
                    parts = lines[0].split(",")
                    if len(parts) >= 2:
                        profile.gpu_name = parts[0].strip()
                        profile.gpu_vendor = "nvidia"
                        try:
                            # e.g., "16384 MiB"
                            vram_str = parts[1].strip().split()[0]
                            profile.vram_gb = float(vram_str) / 1024.0
                        except ValueError:
                            pass

            # Get CUDA version
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False
            )
            if result.returncode == 0 and result.stdout:
                # We could run nvcc or check driver_version. Let's just set a dummy cuda_version for now based on driver if we need it.
                # Since we just need to detect *a* CUDA version for the tier, we'll mark it present.
                profile.cuda_version = "present"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # Determine tier
        profile.tier = self._determine_tier(profile)

        return profile

    def _determine_tier(self, profile: HardwareProfile) -> int:
        """Determines the hardware tier (1-5) based on specs."""
        if profile.gpu_vendor == "nvidia" and profile.vram_gb is not None:
            if profile.vram_gb >= 24:
                return 1
            elif profile.vram_gb >= 10:
                return 2
            elif profile.vram_gb >= 6:
                return 3
            else:
                return 4

        # If no GPU or low VRAM, it's CPU only tier
        return 5
