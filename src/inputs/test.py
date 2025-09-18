# test_rocket.py
from dataclasses import asdict
from src.design.desvar_misreqs import DesignVariables, MissionRequirements
from src.utils.constants import NoseconeType, Material, TubeDiameter, FinAirfoil, TailType
from src.motors.motors import Motor

# ----------------------------
# Mission requirements
# ----------------------------
mission_reqs = MissionRequirements(
    rail_length = 5.6388,           # [m] from LC requirements 18.5ft rail
    payload_mass = 2.0,             # kg
    payload_volume = 0.004,         # m^3
    recovery_mass = 1.5,            # kg
    recovery_volume = 0.006,        # m^3
    propulsion_struct_mass = 3.5,
    coupler_mass = 0.5,
)

# ----------------------------
# Design variables
# ----------------------------
desvars = DesignVariables(
    # Nosecone
    nosecone_type = NoseconeType.CONICAL,
    nosecone_length = 0.55,
    nosecone_material = Material.ALUMINUM,
    nosecone_thickness = 0.004,

    # Fuselage
    tube = TubeDiameter.D6pt0IN,
    upper_fuselage_length = 1.00,
    upper_fuselage_material = Material.ALUMINUM,
    upper_fuselage_thickness = 0.0025,
    lower_fuselage_length = 0.80,
    lower_fuselage_material = Material.ALUMINUM,
    lower_fuselage_thickness = 0.0025,

    # Fins
    fin_airfoil = FinAirfoil.FLATPLATE,
    fin_num = 4,
    fin_area_total = 0.024,      # m^2 (all fins combined)
    fin_material = Material.ALUMINUM,
    fin_aspect_ratio = 2.5,
    fin_taper_ratio = 0.6,
    fin_thickness = 0.004,
    fin_cant=0.0,
    distance_to_fin = 0.10,

    # Tail
    tail_type = TailType.NONE,
    boattail_bot_radius = TubeDiameter.D6pt0IN.value,
    boattail_length = TubeDiameter.D6pt0IN.value,
    boattail_thickness = 0.1,
    boattail_material = Material.ALUMINUM,
    boattail_position = 1,

    # Motor (your enum with RocketPy SolidMotor inside)
    motor_type = Motor.M1790,
)

# Quick print for debugging
print("Mission requirements:")
for k,v in asdict(mission_reqs).items():
    print(f"  {k}: {v}")

print("\nDesign variables:")
for k,v in asdict(desvars).items():
    print(f"  {k}: {v}")
