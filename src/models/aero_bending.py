import numpy as np

def aero_bending(t, config, flight, mm): #NOTE: FLIGHT HAS ROCKET AS AN ATTRIBUTE
    """
    Todo: solve shear and bending moment according to missile design textbook,
    then solve rocket as a simple beam to get bending and shear stress
    """

    mass = flight.rocket.total_mass(t)

    cg = flight.rocket.center_of_mass(t)   # m from nozzle exit
    cp = flight.rocket.cp_position(t)      # m from nozzle exit

    moment_arm_cp_cg = cp - cg  # positive if CP is above CG







    return 1
    
