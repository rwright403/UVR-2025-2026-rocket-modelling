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
    #fin_type: FinType              # currently only TRAPEZOIDAL supported
    fin_airfoil: FinAirfoil        # currently only FLAT PLATE supported
    fin_num: int                   # number of fins (3 or 4)
    fin_area_total: float          # total planform area (all fins) [m^2]
    fin_aspect_ratio: float        # AR = span^2 / area_per_fin
    fin_taper_ratio: float = 0.6   # tip-to-root chord ratio (ct/cr)
    fin_thickness: float           # thickness [m]
    #fin_cant: float = 0.0          # cant angle [deg]
    distance_to_fin: float = 0.0   # axial distance from tail to fin root LE (RocketPy convention)


    # -------------------------
    # Tail / boattail
    # -------------------------
    tail_type: TailType
    boattail_bot_radius: float = 0.0
    boattail_length: float = 0.0

    # -------------------------
    # Motor
    # -------------------------
    motor_type: Motor
    
    # -------------------------
    # Internals
    # -------------------------
    payload_mass: float
    payload_volume: float

    recovery_mass: float
    recovery_volume: float

    propulsion_struct_mass: float #

    coupler_mass: float #TODO: ADD IF FUSE LENGTH INCREASES OR IF UPPER AND LOWER FUSELAGE ARE TWO DIFFERENT MATS


