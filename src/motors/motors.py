from enum import Enum
from rocketpy import SolidMotor

class Motor(Enum):
    CTI_PRO38_2G = SolidMotor(
        thrustSource="motors/Cesaroni_38mm.eng",  # file path
        burnOut=2.5,
        grainNumber=5,
        grainSeparation=0.002,
        grainDensity=1815,
        grainOuterRadius=0.019,
        grainInitialInnerRadius=0.006,
        grainInitialHeight=0.12,
        nozzleRadius=0.009,
        throatRadius=0.005,
        interpolationMethod="linear"
    )
