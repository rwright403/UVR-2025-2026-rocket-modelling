import numpy as np

#TODO: CNa depends on actual geometry

def compute_cp(desvars, total_length, Mach=0.3):
    """
    Compute CP location in tail=0 coordinate system (consistent with compute_geometry).
    """

    r = desvars.tube.radius
    A_ref = np.pi * r**2

    # ---------------------
    # Nosecone contribution
    CNa_nose = 2.0
    # location = 2/3 back from tip
    x_nose = total_length - (2/3) * desvars.nosecone_length

    # ---------------------
    # Fin contribution
    s = desvars.fin_span
    cr = desvars.fin_root_chord
    ct = desvars.fin_tip_chord
    N = desvars.fin_num

    S_fin = 0.5 * (cr + ct) * s  # planform area of one fin
    AR = (s**2) / S_fin
    eta = 0.95

    beta = 1.0 if Mach < 1 else np.sqrt(Mach**2 - 1)

    CL_alpha_fin = (2*np.pi*AR) / (2 + np.sqrt(4 + (AR*beta/eta)**2))
    CNa_fins = N * CL_alpha_fin * (S_fin / A_ref)

    # Fin CP location (measured from fin root leading edge)
    x_fin_ac = (cr/3) * (cr + 2*ct) / (cr + ct) + (1/6) * (
        cr + ct - (cr*ct) / (cr + ct)
    )

    # In tail=0, fin root LE is at motor/fin section start
    fin_root_pos = desvars.propulsion_struct_position  # or tail reference (0)
    x_fins = fin_root_pos + x_fin_ac

    # ---------------------
    # Total CP
    CNa_total = CNa_nose + CNa_fins
    x_cp = (CNa_nose*x_nose + CNa_fins*x_fins) / CNa_total

    return x_cp
