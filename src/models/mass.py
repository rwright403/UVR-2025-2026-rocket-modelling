import numpy as np
from dataclasses import dataclass
from src.utils.constants import *



@dataclass
class mass:
    mass: float
    cg: np.ndarray 
    inertia: np.ndarray # 3x3 Inertia Tensor



def parallel_axis(mass_objs: list):
    """
    Input: list of mass objects

    Returns a mass object representing the total mass and inertia of the list 
    """

    mass_total = sum(mass_obj.mass for mass_obj in mass_objs)

    cg_total = sum(mass_obj.mass * np.array(mass_obj.cg) for mass_obj in mass_objs) / mass_total

    I_total = np.zeros((3, 3))
    for mass_obj in mass_objs:
        m = mass_obj.mass
        d = mass_obj.cg - cg_total
        d2 = np.dot(d, d)

        # Parallel axis contribution
        I_shift = mass_obj.inertia + m * (d2 * np.eye(3) - np.outer(d, d))
        I_total += I_shift

    return mass(mass_total, cg_total, I_total)



def nosecone_mass(radius, nose_type, nose_power, nose_mat, nose_thick, nose_len, total_len):
    """
    Compute mass object for the nosecone.
    
    Parameters
    ----------
    radius : float
        Rocket outer radius [m].
    nose_type : NoseconeType
        Enum specifying nosecone shape.
    nose_power : float
        Power exponent for power-series nosecones (ignored otherwise).
    nose_mat : Material
        Material enum (with .rho density).
    nose_thick : float
        Wall thickness [m].
    nose_len : float
        Nosecone length [m].
    total_len : float
        Total rocket length [m] (tail=0 csys).
    
    Returns
    -------
    mass
        Mass dataclass object for nosecone.
    """

    # Approximate as thin shell of revolution
    R_outer = radius
    R_inner = radius - nose_thick

    # Volume depends on profile
    if nose_type == NoseconeType.LV_HAACK:
        V = (1/3) * np.pi * (R_outer**2 - R_inner**2) * nose_len
        cg_from_tip = 0.437 * nose_len

    elif nose_type == NoseconeType.VON_KARMAN:
        V = (1/3) * np.pi * (R_outer**2 - R_inner**2) * nose_len
        cg_from_tip = 0.466 * nose_len

    elif nose_type == NoseconeType.CONICAL:
        V = (1/3) * np.pi * (R_outer**2 - R_inner**2) * nose_len
        cg_from_tip = 0.75 * nose_len

    elif nose_type == NoseconeType.OGIVE:
        V = (np.pi * nose_len / 6) * (3 * (R_outer**2 - R_inner**2) + (nose_len**2) / 4)
        cg_from_tip = 0.466 * nose_len

    elif nose_type == NoseconeType.POWER_SERIES:
        V = (np.pi * (R_outer**2 - R_inner**2) * nose_len) / (2 * nose_power + 1)
        cg_from_tip = (2 * nose_power + 1) / (2 * nose_power + 3) * nose_len

    else:
        raise ValueError(f"Unsupported nosecone type: {nose_type}")

    m = V * nose_mat.rho

    # Convert cg to tail=0 coordinate system
    x_cg = total_len - nose_len + cg_from_tip
    cg = np.array([x_cg, 0.0, 0.0])
    I = np.zeros((3, 3))  # point mass approx

    return mass(m, cg, I)



def upper_fuselage_mass(mass_mat, radius: float, thickness: float,
                        upper_fuse_len: float, lower_fuse_len: float,
                        boattail_len: float = 0.0):
    """
    Create a mass object for the upper fuselage section (cylindrical shell).

    Parameters
    ----------
    mass_mat : Material
        Material enum with .rho (density).
    radius : float
        Outer radius of fuselage [m].
    thickness : float
        Wall thickness [m].
    upper_fuse_len : float
        Length of upper fuselage [m].
    lower_fuse_len : float
        Length of lower fuselage [m].
    boattail_len : float, optional
        Length of boattail [m], default = 0.0.

    Returns
    -------
    mass
        Mass dataclass object for upper fuselage.
    """

    R_outer = radius
    R_inner = radius - thickness
    L = upper_fuse_len

    # Volume of shell
    vol = np.pi * (R_outer**2 - R_inner**2) * L
    m = vol * mass_mat.rho

    # Centroid (tail=0 coords)
    x_cg = boattail_len + lower_fuse_len + 0.5 * L
    cg = np.array([x_cg, 0.0, 0.0])

    # Inertia (approx thin cylinder)
    Ixx = 0.5 * m * (R_outer**2 + R_inner**2)
    Iyy = Izz = (1/12) * m * (3*(R_outer**2 + R_inner**2) + L**2)

    return mass(m, cg, np.diag([Ixx, Iyy, Izz]))



def lower_fuselage_mass(mass_mat, radius: float, thickness: float,
                        lower_fuse_len: float, boattail_len: float = 0.0):
    """
    Create a mass object for the lower fuselage section (cylindrical shell).

    Parameters
    ----------
    mass_mat : Material
        Material enum with .rho (density).
    radius : float
        Outer radius of fuselage [m].
    thickness : float
        Wall thickness [m].
    lower_fuse_len : float
        Length of lower fuselage [m].
    boattail_len : float, optional
        Length of boattail [m], default = 0.0.

    Returns
    -------
    mass
        Mass dataclass object for lower fuselage.
    """

    R_outer = radius
    R_inner = radius - thickness
    L = lower_fuse_len

    # Volume of shell
    vol = np.pi * (R_outer**2 - R_inner**2) * L
    m = vol * mass_mat.rho

    # Centroid (tail=0 coords)
    x_cg = boattail_len + 0.5 * L
    cg = np.array([x_cg, 0.0, 0.0])

    # Inertia (approx thin cylinder)
    Ixx = 0.5 * m * (R_outer**2 + R_inner**2)
    Iyy = Izz = (1/12) * m * (3*(R_outer**2 + R_inner**2) + L**2)

    return mass(m, cg, np.diag([Ixx, Iyy, Izz]))



def fin_mass():
    #sol volume of one fin
    #multiply by material density and number of fins

    return mass



def boattail_mass(radius_top: float, radius_bot: float, length: float,
                  thickness: float, mat, x0: float = 0.0):
    """
    Mass model for a conical boattail (frustum shell).
    
    Parameters
    ----------
    radius_top : float
        Outer radius at fuselage junction [m].
    radius_bot : float
        Outer radius at aft end [m].
    length : float
        Boattail length [m].
    thickness : float
        Wall thickness [m].
    mat : Material
        Material enum with .rho (density).
    x0 : float, optional
        Starting position of boattail (tail=0). Default=0.
    
    Returns
    -------
    mass
        Mass dataclass object for boattail.
    """

    if length <= 0:
        return mass(0.0, np.array([x0, 0, 0]), np.zeros((3, 3)))

    # Outer & inner radii
    Rt, Rb = radius_top, radius_bot
    Rti, Rbi = Rt - thickness, Rb - thickness

    # Volume of hollow frustum
    V = (np.pi * length / 3.0) * (
        (Rt**2 + Rt*Rb + Rb**2) - (Rti**2 + Rti*Rbi + Rbi**2)
    )
    m = V * mat.rho

    # Centroid from boattail base (tail=0 at x0)
    num = (Rt**2 + 2*Rt*Rb + 3*Rb**2) - (Rti**2 + 2*Rti*Rbi + 3*Rbi**2)
    den = (Rt**2 + Rt*Rb + Rb**2) - (Rti**2 + Rti*Rbi + Rbi**2)
    
    x_cg = x0 + length * (num / (4 * den))
    cg = np.array([x_cg, 0.0, 0.0])
    I = np.zeros((3, 3))  # point mass approx

    return mass(m, cg, I)



def motor_wet_mass(motor, t: float = 0.0):
    """
    Compute wet motor mass, inertia, and CG from a RocketPy SolidMotor object.

    Parameters
    ----------
    motor : SolidMotor
        RocketPy motor object (fully defined with geometry + mass).
    t : float, optional
        Time [s] at which to evaluate properties. Default = 0 (pre-ignition).

    Returns
    -------
    dict
        Dictionary with:
        - "mass" : float, total motor mass [kg]
        - "cg"   : np.ndarray, center of mass [m] in motor CSYS
        - "inertia" : np.ndarray, inertia tensor [kg·m²] about CG
    """

    # Total mass = dry + propellant at time t
    m_total = motor.total_mass(t)

    # CG location at time t
    x_cg = motor.center_of_mass(t)
    cg = np.array([x_cg, 0.0, 0.0])

    # Inertia components at time t
    I11 = motor.I_11(t)
    I22 = motor.I_22(t)
    I33 = motor.I_33(t)

    # Cross-terms (usually 0 by symmetry)
    I12 = motor.I_12(t)
    I13 = motor.I_13(t)
    I23 = motor.I_23(t)

    inertia = np.array([
        [I11, I12, I13],
        [I12, I22, I23],
        [I13, I23, I33]
    ])

    return {
        "mass": m_total,
        "cg": cg,
        "inertia": inertia
    }



def recovery_mass(mass_val: float, recovery_vol: float, radius: float, total_len: float, nose_len: float):
    """
    Create a mass object for the recovery system (parachute, harness, etc.).
    Centroid: halfway along recovery bay, just aft of nosecone.
    Inertia: point mass approximation.

    Parameters
    ----------
    mass_val : float
        Recovery system mass [kg].
    recovery_vol : float
        Recovery bay volume [m^3].
    radius : float
        Rocket outer radius [m].
    total_len : float
        Total rocket length [m] (tail=0 coords).
    nose_len : float
        Nosecone length [m].

    Returns
    -------
    mass
        Mass dataclass object for recovery system.
    """

    # Solve recovery bay length from volume constraint
    A_tube = np.pi * radius**2
    L_recovery = recovery_vol / A_tube

    # CG position (tail=0 csys)
    x_cg = total_len - nose_len - 0.5 * L_recovery
    cg = np.array([x_cg, 0.0, 0.0])
    I = np.zeros((3, 3))  # point mass

    return mass(mass_val, cg, I)



def propulsion_struct_mass(mass_val: float, pro98_len: float):
    """
    Create a mass object for the propulsion structure.
    Assumes centroid is at motor centroid (half Pro98 length from tail).
    Inertia taken as point mass (zeros).
    
    Parameters
    ----------
    mass_val : float
        Propulsion structure mass [kg].
    pro98_len : float
        Motor length [m].
    
    Returns
    -------
    mass
        Mass dataclass object.
        Inertia about its own cg aligned w global csys
    """
    x_cg = 0.5 * pro98_len
    cg = np.array([x_cg, 0.0, 0.0])
    I = np.zeros((3, 3))  # point mass

    return mass(mass_val, cg, I)



def coupler_mass(mass_val: float, lower_fuse_len: float, boattail_len: float = 0.0):
    """
    Create a mass object for the coupler between upper and lower fuselage.
    Centroid: at the junction (end of lower fuselage + boattail).
    Inertia: point mass approximation.

    Parameters
    ----------
    mass_val : float
        Coupler mass [kg].
    lower_fuse_len : float
        Length of lower fuselage [m].
    boattail_len : float, optional
        Length of boattail [m], default = 0.0 if no boattail.

    Returns
    -------
    mass
        Mass dataclass object for coupler.
    """

    x_cg = boattail_len + lower_fuse_len
    cg = np.array([x_cg, 0.0, 0.0])
    I = np.zeros((3, 3))  # point mass

    return mass(mass_val, cg, I)



def payload_mass(mass_val: float, payload_vol: float, radius: float,
                 total_len: float, nose_len: float, recovery_vol: float):
    """
    Create a mass object for the payload system.
    Centroid: halfway along payload bay, aft of recovery system.
    Inertia: point mass approximation.

    Parameters
    ----------
    mass_val : float
        Payload mass [kg].
    payload_vol : float
        Payload bay volume [m^3].
    radius : float
        Rocket outer radius [m].
    total_len : float
        Total rocket length [m] (tail=0 coords).
    nose_len : float
        Nosecone length [m].
    recovery_vol : float
        Recovery bay volume [m^3].

    Returns
    -------
    mass
        Mass dataclass object for payload system.
    """

    A_tube = np.pi * radius**2

    # Solve lengths from volumes
    L_recovery = recovery_vol / A_tube
    L_payload = payload_vol / A_tube

    # CG position (tail=0 coords)
    x_cg = total_len - nose_len - L_recovery - 0.5 * L_payload
    cg = np.array([x_cg, 0.0, 0.0])
    I = np.zeros((3, 3))  # point mass

    return mass(mass_val, cg, I)



class MassModel:
    def __init__(self, config):
        """
        Build point mass model from config dataclass (geometry + materials).
        """
        self.config = config
        self.parts = self._build_parts(config)  # dict of part -> mass dataclass
        self.motor = None  # filled later if needed

    def _build_parts(self, cfg):
        """Return dict of all point masses."""
        parts = {}

        parts["nosecone"] = nosecone_mass(
            cfg.tube.radius, cfg.nosecone_type, cfg.nosecone_power,
            cfg.nosecone_material, cfg.nosecone_thickness,
            cfg.nosecone_length, cfg.total_length
        )

        parts["upper_fuselage"] = upper_fuselage_mass(
            cfg.upper_fuselage_material, cfg.tube.radius,
            cfg.upper_fuselage_thickness, cfg.upper_fuselage_length,
            cfg.lower_fuselage_length, cfg.boattail_length
        )

        parts["lower_fuselage"] = lower_fuselage_mass(
            cfg.lower_fuselage_material, cfg.tube.radius,
            cfg.lower_fuselage_thickness, cfg.lower_fuselage_length,
            cfg.boattail_length
        )

        parts["fins"] = fin_mass(

            
        )  # TODO: expand like nosecone with geom + mat

        parts["boattail"] = boattail_mass(
            cfg.tube.radius, cfg.boattail_bot_radius,
            cfg.boattail_length, cfg.boattail_thickness,
            cfg.boattail_material, x0=0.0
        )

        parts["recovery"] = recovery_mass(
            cfg.recovery_mass, cfg.recovery_volume,
            cfg.tube.radius, cfg.total_length, cfg.nosecone_length
        )

        parts["prop_struct"] = propulsion_struct_mass(
            cfg.propulsion_struct_mass, cfg.pro98_len
        )

        parts["coupler"] = coupler_mass(
            cfg.coupler_mass, cfg.lower_fuselage_length, cfg.boattail_length
        )

        parts["payload"] = payload_mass(
            cfg.payload_mass, cfg.payload_volume,
            cfg.tube.radius, cfg.total_length,
            cfg.nosecone_length, cfg.recovery_volume
        )

        parts["motor"] = motor_wet_mass(motor=cfg.motor_type)

        self.parts = parts

    def wet_mass(self) -> mass:
        """Equivalent point mass for wet mass rocket"""
        return parallel_axis(list(self.parts.values()))


    def rocketpy_tuple(self):
        """
        Export dry rocket to RocketPy convention:
        (mass, (Ixx, Iyy, Izz), cg list)
        """
        rktpy_parts = {k: v for k, v in self.parts.items() if k != "motor"}
        m_obj = parallel_axis(list(rktpy_parts.values()))
        return (
            m_obj.mass,
            tuple(m_obj.inertia.diagonal()),
            m_obj.cg.tolist()
        )