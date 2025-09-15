# src/design/config.py

from dataclasses import dataclass
import numpy as np
from src.design.desvars import DesignVariables, NoseconeType, TubeDiameter, Material
from src.design.missionreqs import MissionRequirements

# -------------------------
# Helpers
# -------------------------

def derive_trapezoid_geometry(A_total: float, fin_num: int,
                              AR: float, taper_ratio: float = 0.6):
    """
    Derive trapezoidal fin geometry from area, aspect ratio, and taper ratio.
    """
    A_fin = A_total / fin_num
    span = np.sqrt(AR * A_fin)
    c_avg = A_fin / span
    c_r = 2 * c_avg / (1 + taper_ratio)
    c_t = taper_ratio * c_r
    return span, c_r, c_t


# -------------------------
# Config (merged + derived)
# -------------------------

@dataclass
class Config:
    # Nosecone
    nosecone_type: NoseconeType
    nosecone_length: float
    nosecone_material: Material
    nosecone_thickness: float
    nosecone_power: float | None = None

    # Fuselage
    tube: TubeDiameter
    upper_fuselage_length: float
    upper_fuselage_material: Material
    upper_fuselage_thickness: float
    lower_fuselage_length: float
    lower_fuselage_material: Material
    lower_fuselage_thickness: float

    # Fins (reduced param set)
    fin_num: int
    fin_area_total: float
    fin_aspect_ratio: float
    fin_taper_ratio: float
    fin_thickness: float
    fin_cant: float = 0.0
    distance_to_fin: float = 0.0

    # Derived fin geometry
    fin_span: float = 0.0
    fin_root_chord: float = 0.0
    fin_tip_chord: float = 0.0
    fin_sweep_length: float = 0.0
    fin_sweep_angle: float = 0.0

    # Tail
    boattail_bot_radius: float = 0.0
    boattail_length: float = 0.0
    boattail_thickness: float = 0.0
    boattail_material: Material | None = None

    # Internals / mission
    payload_mass: float = 0.0
    payload_volume: float = 0.0
    recovery_mass: float = 0.0
    recovery_volume: float = 0.0
    propulsion_struct_mass: float = 0.0
    coupler_mass: float = 0.0

    # -------------------------
    # Methods
    # -------------------------

    def derive(self):
        """Compute derived fin geometry and update fields."""
        span, cr, ct = derive_trapezoid_geometry(
            A_total=self.fin_area_total,
            fin_num=self.fin_num,
            AR=self.fin_aspect_ratio,
            taper_ratio=self.fin_taper_ratio
        )
        self.fin_span = span
        self.fin_root_chord = cr
        self.fin_tip_chord = ct
        self.fin_sweep_length = cr - ct
        self.fin_sweep_angle = np.degrees(np.arctan2(self.fin_sweep_length, span))

    def as_dict(self):
        """Dump everything into a dict (for logging/optimizer)."""
        return self.__dict__.copy()


# -------------------------
# Builder
# -------------------------

def build_config(desvars: DesignVariables, mission: MissionRequirements) -> Config:
    """
    Combine design variables and mission requirements into a Config,
    then derive geometry automatically.
    """
    config = Config(

        rkt_radius = desvars.radius,

        # Nosecone
        nosecone_type=desvars.nosecone_type,
        nosecone_length=desvars.nosecone_length,
        nosecone_material=desvars.nosecone_material,
        nosecone_thickness=desvars.nosecone_thickness,
        nosecone_power=desvars.nosecone_power,

        # Fuselage
        tube=desvars.tube,
        upper_fuselage_length=desvars.upper_fuselage_length,
        upper_fuselage_material=desvars.upper_fuselage_material,
        upper_fuselage_thickness=desvars.upper_fuselage_thickness,
        lower_fuselage_length=desvars.lower_fuselage_length,
        lower_fuselage_material=desvars.lower_fuselage_material,
        lower_fuselage_thickness=desvars.lower_fuselage_thickness,

        # Fins
        fin_num=desvars.fin_num,
        fin_area_total=desvars.fin_area_total,
        fin_material=desvars.fin_material,
        fin_aspect_ratio=desvars.fin_aspect_ratio,
        fin_taper_ratio=desvars.fin_taper_ratio,
        fin_thickness=desvars.fin_thickness,
        fin_cant=desvars.fin_cant,
        distance_to_fin=desvars.distance_to_fin,

        # Tail
        boattail_bot_radius=desvars.boattail_bot_radius,
        boattail_length=desvars.boattail_length,
        boattail_thickness=desvars.boattail_thickness,
        boattail_material=desvars.boattail_material,

        # Mission requirements
        payload_mass=mission.payload_mass,
        payload_volume=mission.payload_volume,
        recovery_mass=mission.recovery_mass,
        recovery_volume=mission.recovery_volume,
        propulsion_struct_mass=mission.propulsion_struct_mass,
        coupler_mass=mission.coupler_mass
    )

    # Derive fin geometry etc.
    config.derive()
    return config
