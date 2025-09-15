import numpy as np
from dataclasses import dataclass
from src.utils.constants import *
from src.motors.motors import *
"""
# NOTE: csys is nose to tail?
"""

@dataclass
class MissionRequirements:

    # -------------------------
    # Internals
    # -------------------------
    payload_mass: float
    payload_volume: float

    recovery_mass: float
    recovery_volume: float

    propulsion_struct_mass: float #

    coupler_mass: float #TODO: ADD IF FUSE LENGTH INCREASES OR IF UPPER AND LOWER FUSELAGE ARE TWO DIFFERENT MATS


