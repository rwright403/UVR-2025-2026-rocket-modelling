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




import numpy as np

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

def boattail_mass():
    #sol volume
    #multiply by material density

    return mass



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






def build_mass_model(desvars):
    """
    Take our design variables and solve rocketpy mass params
    NOTE: rocketpy requests mass, inertia cm to account for
          entire rocket except rocket motor mass (both wet and dry)
    """
    rkt_pt_masses = [
        nosecone_mass(desvars.nose_type, desvars.nose_mat, desvars.nose_thick, desvars.nose_len),
        upper_fuselage_mass(),
        lower_fuselage_mass(),
        fin_mass(),
        boattail_mass(),
        recovery_mass(),
        propulsion_struct_mass(),
        coupler_mass(),
        payload_mass(),
    ]

    # Parallel axis to get overall rocket mass obj

    rocket_mass = parallel_axis(rkt_pt_masses)

    #TODO: NEED TO ADD MOTOR TO CHECK STABLE, THEN REMOVE IT FOR ROCKETPY

    # Format to Rocketpy Convention #NOTE: split this up? we want pt masses w inertia for aero bending!
    rp_mass = rocket_mass.mass
    rp_inertia = tuple(rocket_mass.inertia.diagonal())  # RocketPy expects tuple
    rp_cm = rocket_mass.cg.tolist()

    return rp_mass, rp_inertia, rp_cm,