import numpy as np

def aero_bending(desvars, mission, flight, SM_min=1.5, FOS=1.5):
    """
    Full shear/bending beam model at max Q.
    """

    # 1. Get max Q flight condition
    q_max = np.max(flight.dynamic_pressure)
    idx = np.argmax(flight.dynamic_pressure)
    V = flight.v[idx]
    rho = flight.rho[idx]
    alpha = flight.angle_of_attack[idx]
    a_n = flight.a[idx]  # normal accel at max Q

    # 2. Section properties
    def EI(E, R, t):
        I = np.pi * R**3 * t  # thin-shell inertia
        return E * I, I

    EI_lower, I_lower = EI(desvars.lower_fuselage_material.E,
                           desvars.tube.radius,
                           desvars.lower_fuselage_thickness)
    EI_upper, I_upper = EI(desvars.upper_fuselage_material.E,
                           desvars.tube.radius,
                           desvars.upper_fuselage_thickness)

    # 3. Geometry
    L_total = (desvars.boattail_length +
               desvars.lower_fuselage_length +
               desvars.upper_fuselage_length +
               desvars.nosecone_length)

    # 4. Loads
    A_ref = np.pi * desvars.tube.radius**2
    CN_alpha = 2*np.pi  # thin airfoil slope [per rad]
    L_total_force = CN_alpha * alpha * q_max * A_ref  # total lift [N]
    w = L_total_force / L_total  # uniform load [N/m]

    # Point inertial loads (payload, recovery, etc.)
    # -> from your part-level mass objects:
    parts = [
        payload_mass(mission.payload_mass, mission.payload_volume,
                     desvars.tube.radius, L_total,
                     desvars.nosecone_length, mission.recovery_volume),
        recovery_mass(mission.recovery_mass, mission.recovery_volume,
                      desvars.tube.radius, L_total, desvars.nosecone_length),
        propulsion_struct_mass(mission.propulsion_struct_mass, desvars.pro98_len)
    ]

    point_loads = [(p.cg[0], p.mass * a_n) for p in parts]  # (location, force)

    # 5. Shear & moment integration
    npts = 200
    x = np.linspace(0, L_total, npts)
    V = np.zeros_like(x)
    M = np.zeros_like(x)

    for i, xi in enumerate(x):
        # distributed load contribution
        V[i] = w * (L_total - xi)
        # add point forces aft of xi
        for loc, F in point_loads:
            if loc >= xi:
                V[i] += F
        # integrate for moment
        M[i] = np.trapz(V[:i+1], x[:i+1])

    # 6. Stress check
    sigma_lower = np.max(M) * desvars.tube.radius / I_lower
    sigma_upper = np.max(M) * desvars.tube.radius / I_upper

    safe_lower = sigma_lower <= desvars.lower_fuselage_material.sigma_y / FOS
    safe_upper = sigma_upper <= desvars.upper_fuselage_material.sigma_y / FOS

    return {
        "q_max": q_max,
        "sigma_lower": sigma_lower,
        "sigma_upper": sigma_upper,
        "safe_lower": safe_lower,
        "safe_upper": safe_upper,
        "x": x,
        "V": V,
        "M": M
    }
