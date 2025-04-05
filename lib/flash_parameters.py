from dataclasses import dataclass, field

FLASH_DURATION_SECONDS = 0.1
RESETTING_STRENGTH = 0.5


@dataclass
class FlashParameters:
    angular_frequency: float
    phase: float
    duration: float = field(default=FLASH_DURATION_SECONDS)
    resetting_strength: float = field(default=RESETTING_STRENGTH)
