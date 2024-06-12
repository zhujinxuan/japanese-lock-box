from dataclasses import dataclass


# Build config
@dataclass
class BuildConfig:
    nozzle: float = 0.4
    length: float = 160
    width: float = 60
    height: float = 60
    wallThickness: float = 2
    lidPanelLength: float = 20
    lidBotomDelta: float = 10
    sildeHorizontalAngle: float = 7
    slideTaper: float = 30
    lidThicknessTop: float = 2
    lidThicknessBelow: float = 2
    filletRadius: float = 1
