from dataclasses import dataclass
import numpy as np

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