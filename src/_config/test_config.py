from src.design.desvars import DesignVariables
from src.utils.constants import TubeDiameter, Material, NoseconeType, FinType, TailType, FinAirfoil

desvars = DesignVariables(
    nosecone_type=NoseconeType.CONICAL,
    nosecone_length=0.5,
    nosecone_material=Material.CARBON_FIBER,
    nosecone_thickness=0.003,

    tube=TubeDiameter.D4pt5IN,
    upper_fuselage_length=0.8,
    upper_fuselage_material=Material.ALUMINUM,
    upper_fuselage_thickness=0.002,
    lower_fuselage_length=0.6,
    lower_fuselage_material=Material.ALUMINUM,
    lower_fuselage_thickness=0.002,

    fin_type=FinType.TRAPEZOIDAL,
    fin_airfoil=FinAirfoil.FLATPLATE,
    fin_num=3,
    fin_root_chord=0.15,
    fin_tip_chord=0.05,
    fin_span=0.08,
    fin_thickness=0.004,
    distance_to_cg=0.4,

    tail_type=TailType.CONICAL,
    boattail_bot_radius=0.04,
    boattail_length=0.1
)
