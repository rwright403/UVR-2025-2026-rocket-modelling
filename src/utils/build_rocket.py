import numpy as np
from uvicrocketpy import Rocket
from src.utils.constants import *
from src.models.mass import MassModel
#from src.models.drag import build_drag_model

def build_rocket(config):
    
    mm = MassModel(config)
    rp_mass, rp_inertia, rp_cm = mm.rocketpy_tuple()

    print("mm out: ", rp_mass, rp_inertia, rp_cm)


    #cd_power_on, cd_power_off = build_drag_model(config)
    cd_power_on="src/models/powerOnDragCurve.csv"
    cd_power_off="src/models/powerOffDragCurve.csv"


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
    rocket.add_nose(
        length=config.nosecone_length,
        position=config.nosecone_pos,
        kind=config.nosecone_type.value,
        power=config.nosecone_power
    )

    # Fins

    rocket.add_trapezoidal_fins(
        n=config.fin_num,
        span=config.fin_span,
        root_chord=config.fin_root_chord,
        tip_chord=config.fin_tip_chord,
        position=config.distance_to_fin,
        cant_angle=config.fin_cant,
        sweep_length=config.fin_sweep_length,
        airfoil=None
    )


    # Tail
    # TODO: BOATTAIL VS NO BOATTAIL
    rocket.add_tail(
        top_radius=config.tube.radius,
        bottom_radius=config.boattail_bot_radius,
        length=config.boattail_length,
        position=config.boattail_position
    )

    rocket.set_rail_buttons(
        upper_button_position=pro98_len,
        lower_button_position=-0.0,
        angular_position=45,
    )

    #rocket.add_motor(config.motor_type, config.motor_pos)
    rocket.add_motor(config.motor_type.value, 0.0)
                                        #NOTE: is this just 0 ???
    return rocket, mm
