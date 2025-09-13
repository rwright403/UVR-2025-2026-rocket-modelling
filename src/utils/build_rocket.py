import numpy as np
from rocketpy import Rocket
from src.utils.constants import *
from src.models.mass import build_mass_model
from src.models.drag import build_drag_model

def build_rocket(desvars):
    rp_mass, rp_inertia, rp_cm = build_mass_model(desvars) #Mass model creates a stable config
    cd_power_on, cd_power_off = build_drag_model(desvars)
    #TODO: fin lift model!

    # From mass model assembly everything according to rocketpy
    rocket = Rocket(
        radius=desvars.tube.radius,
        mass=rp_mass,
        inertia=rp_inertia,
        power_off_drag=cd_power_off,
        power_on_drag=cd_power_on,
        center_of_mass_without_motor=rp_cm,
        coordinate_system_orientation="tail_to_nose"
    )

    # Nosecone
    rocket.add_nosecone(
        length=desvars.nosecone_length,
        kind=desvars.nosecone_type.value,
        power=desvars.nosecone_power
    )

#TODO: ADD LIFT MODEL!!!
    # Fins
    if desvars.fin_type == FinType.TRAPEZOIDAL:
        rocket.add_trapezoidal_fins(
            number_of_fins=desvars.fin_num,
            span=desvars.fin_span,
            root_chord=desvars.fin_root_chord,
            tip_chord=desvars.fin_tip_chord,
            distance_to_cg=desvars.distance_to_cg,
            cant_angle=desvars.fin_cant,
            sweep_length=desvars.fin_sweep_length,
            sweep_angle=desvars.fin_sweep_angle,
            airfoil=None if desvars.fin_airfoil == FinAirfoil.FLATPLATE
                   else (lambda alpha: 2*np.pi*alpha, "radians")
        )
    elif desvars.fin_type == FinType.ELLIPTICAL:
        rocket.add_elliptical_fins(
            number_of_fins=desvars.fin_num,
            span=desvars.fin_span,
            root_chord=desvars.fin_root_chord,
            distance_to_cg=desvars.distance_to_cg,
            cant_angle=desvars.fin_cant,
            airfoil=None if desvars.fin_airfoil == FinAirfoil.FLATPLATE
                   else (lambda alpha: 2*np.pi*alpha, "radians")
        )

    # Tail
    if desvars.tail_type != TailType.NONE:
        rocket.add_tail(
            top_radius=desvars.tube.radius,
            bottom_radius=desvars.boattail_bot_radius,
            length=desvars.boattail_length
        )

    rocket.set_rail_buttons(
        upper_button_position=pro98_len,
        lower_button_position=-0.0,
        angular_position=45,
    )

    return rocket
