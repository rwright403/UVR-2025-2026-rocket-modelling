import numpy as np
from rocketpy import Rocket
from src.utils.constants import *
from src.utils.build_config import build_config
from src.models.mass import MassModel
from src.models.drag import build_drag_model

def build_rocket(desvars, missionreqs):

    config = build_config(desvars, missionreqs)
    
    mm = MassModel(config)
    rp_mass, rp_inertia, rp_cm = mm.rocketpy_tuple()

    cd_power_on, cd_power_off = build_drag_model(config)

    #TODO: fin lift model!

    # From mass model assembly everything according to rocketpy
    rocket = Rocket(
        radius=config.tube.radius,
        mass=rp_mass,
        inertia=rp_inertia,
        power_off_drag=cd_power_off,
        power_on_drag=cd_power_on,
        center_of_mass_without_motor=rp_cm,
        coordinate_system_orientation="tail_to_nose"
    )

    # Nosecone
    rocket.add_nosecone(
        length=config.nosecone_length,
        kind=config.nosecone_type.value,
        power=config.nosecone_power
    )

#TODO: ADD LIFT MODEL!!!
    # Fins
    if config.fin_type == FinType.TRAPEZOIDAL:
        rocket.add_trapezoidal_fins(
            number_of_fins=config.fin_num,
            span=config.fin_span,
            root_chord=config.fin_root_chord,
            tip_chord=config.fin_tip_chord,
            distance_to_cg=config.distance_to_cg,
            cant_angle=config.fin_cant,
            sweep_length=config.fin_sweep_length,
            sweep_angle=config.fin_sweep_angle,
            airfoil=None if config.fin_airfoil == FinAirfoil.FLATPLATE
                   else (lambda alpha: 2*np.pi*alpha, "radians")
        )
    else:
        raise NotImplementedError

    # Tail
    if config.tail_type != TailType.NONE:
        rocket.add_tail(
            top_radius=config.tube.radius,
            bottom_radius=config.boattail_bot_radius,
            length=config.boattail_length
        )

    rocket.set_rail_buttons(
        upper_button_position=pro98_len,
        lower_button_position=-0.0,
        angular_position=45,
    )

    return rocket
