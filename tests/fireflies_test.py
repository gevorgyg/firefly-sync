from numpy import pi
from fireflies import Firefly


def test_firefly_creation():
    firefly = Firefly(id=100, freq_rad_s=pi, phase_rad=0.0)
    assert firefly.id == 100
    assert firefly.freq_rad_s - pi < 1e-6
    assert firefly.phase_rad == 0.0


def test_firefly_advance_phase():
    firefly = Firefly(id=1, freq_rad_s=pi / 2, phase_rad=pi / 2, flash_threshold=2 * pi)
    firefly.advance_phase(1.0)  # Advance by 1 second
    assert firefly.phase_rad - pi < 1e-6  # Phase should be pi after advancing
    firefly.advance_phase(2.0)
    assert firefly.is_flashing()  # Should be flashing after reaching the threshold
    firefly.reset()
    assert firefly.phase_rad == 0.0  # The phase should reset to 0 after reset
    assert firefly.is_waiting()
