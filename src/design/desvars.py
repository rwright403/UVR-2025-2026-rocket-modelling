import numpy as np
from dataclasses import dataclass
from src.utils.constants import *
from src.motors.motors import *
from src.models.barrowman_cp import *
"""
# NOTE: csys is nose to tail?
"""

@dataclass
class DesignVariables:
    # -------------------------
    # Nosecone
    # -------------------------
    nosecone_type: NoseconeType
    nosecone_length: float
    nosecone_material: Material
    nosecone_thickness: float
    nosecone_power: float | None = None  # only used if powerSeries

    # -------------------------
    # Fuselage
    # -------------------------
    tube: TubeDiameter
    upper_fuselage_length: float
    upper_fuselage_material: Material
    upper_fuselage_thickness: float
    lower_fuselage_length: float
    lower_fuselage_material: Material
    lower_fuselage_thickness: float

    # -------------------------
    # Fins
    # -------------------------
    fin_type: FinType
    fin_airfoil: FinAirfoil
    fin_num: int
    fin_root_chord: float
    fin_tip_chord: float
    fin_span: float
    fin_thickness: float
    fin_cant: float = 0.0
    fin_sweep_length: float | None = None
    fin_sweep_angle: float | None = None
    distance_to_cg: float = 0.0  # RocketPy requires it

    # -------------------------
    # Tail / boattail
    # -------------------------
    tail_type: TailType
    boattail_bot_radius: float = 0.0
    boattail_length: float = 0.0

    # -------------------------
    # Internals
    # -------------------------
    payload_mass: float
    payload_volume: float

    recovery_mass: float
    recovery_volume: float

    propulsion_struct_mass: float #

    coupler_mass: float #TODO: ADD IF FUSE LENGTH INCREASES OR IF UPPER AND LOWER FUSELAGE ARE TWO DIFFERENT MATS


