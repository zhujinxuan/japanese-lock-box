from dataclasses import dataclass


# Build config
@dataclass
class BuildConfig:
    tolerence: float = 0.2
    length: float = 160
    width: float = 80
    height: float = 100
    wallThickness: float = 4
    leftPanelWidth: float = 20
    rightPanelWidth: float = 20
    lidPanelWidth: float = 20
    lidLockAngle: float = 7
