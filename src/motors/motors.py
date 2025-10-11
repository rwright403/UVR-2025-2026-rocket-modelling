from enum import Enum
from uvicrocketpy import SolidMotor

### NOTE: Assumptions:
# grain_initial_inner_radius=throat_radius
# grains_center_of_mass_position=center_of_dry_mass_position
# all grain density and grain height same as M1790

class Motor(Enum):
    """
    CTI M1790:
    https://pro38.com/products/p98-4g/8088m1790-p/
    """
    M1790 = SolidMotor(
        thrust_source="./src/motors/Cesaroni_8088M1790-P.eng",
        dry_mass=3.0238,
        dry_inertia=(0.00564,0.21170,0.21170),
        nozzle_radius=0.0301,
        grain_number=4,
        grain_density=5121.683939,
        grain_outer_radius=0.04596,
        grain_initial_inner_radius=0.013195, #assumed same as nozzle throat rad
        grain_initial_height=0.1683173333,
        grain_separation=0.005,
        grains_center_of_mass_position=0.35228, #assumed same as center of dry mass
        center_of_dry_mass_position=0.35228,
        nozzle_position=0.0,
        burn_time=4.53,
        throat_radius=0.013195,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    """
    CTI M1450:
    https://pro38.com/products/p98-4g/9955m1450-p/
    """
    M1450 = SolidMotor(
        thrust_source="./src/motors/Cesaroni_9955M1450-P.eng",
        dry_mass=3.0238,
        dry_inertia=(0.00564,0.21170,0.21170),
        nozzle_radius=0.0301,
        grain_number=4,
        grain_density=5121.683939,
        grain_outer_radius=0.04596,
        grain_initial_inner_radius=0.013195,
        grain_initial_height=0.1683173333,
        grain_separation=0.005,
        grains_center_of_mass_position=0.35228,
        center_of_dry_mass_position=0.35228,
        nozzle_position=0.0,
        burn_time=6.87,
        throat_radius=0.013195,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    """
    CTI M3400:
    https://pro38.com/products/p98-4g/9994M3400-p/
    """
    M3400 = SolidMotor(
        thrust_source="./src/motors/Cesaroni_9994M3400-P.eng",
        dry_mass=3.0238,
        dry_inertia=(0.00564,0.21170,0.21170),
        nozzle_radius=0.0301,
        grain_number=4,
        grain_density=5121.683939,
        grain_outer_radius=0.04596,
        grain_initial_inner_radius=0.013195,
        grain_initial_height=0.1683173333,
        grain_separation=0.005,
        grains_center_of_mass_position=0.35228,
        center_of_dry_mass_position=0.35228,
        nozzle_position=0.0,
        burn_time=2.92,
        throat_radius=0.013195,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    """
    CTI M795:
    https://pro38.com/products/p98-4g/10133M795-p/
    """
    M795 = SolidMotor(
        thrust_source="./src/motors/Cesaroni_10133M795-P.eng",
        dry_mass=3.0238,
        dry_inertia=(0.00564,0.21170,0.21170),
        nozzle_radius=0.0301,
        grain_number=4,
        grain_density=5121.683939,
        grain_outer_radius=0.04596,
        grain_initial_inner_radius=0.013195,
        grain_initial_height=0.1683173333,
        grain_separation=0.005,
        grains_center_of_mass_position=0.35228,
        center_of_dry_mass_position=0.35228,
        nozzle_position=0.0,
        burn_time=None,
        throat_radius=0.013195,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )


    """
    N3400
    https://pro38.com/products/p98-6gxl/14263n3400-p/
    """
    N3400 = SolidMotor(
        thrust_source="./src/motors/Cesaroni_14263N3400-P.eng",
        dry_mass=4.3985,
        dry_inertia=(0.00876,0.8265,0.8265),
        nozzle_radius=0.0301,
        grain_number=6, #NOTE: 6 GRAIN XL CASE
        grain_density=5121.683939,
        grain_outer_radius=0.04596,
        grain_initial_inner_radius=0.013195,
        grain_initial_height=0.1683173333,
        grain_separation=0.005,
        grains_center_of_mass_position=0.35228,
        center_of_dry_mass_position=0.35228,
        nozzle_position=0.0,
        burn_time=4.19,
        throat_radius=0.013195,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    """
    N2540:
    https://pro38.com/products/p98-6gxl/17907n2540-p/
    """
    N2540 = SolidMotor(
        thrust_source="./src/motors/Cesaroni_17907N2540-P.eng",
        dry_mass=4.3985,
        dry_inertia=(0.00876,0.8265,0.8265),
        nozzle_radius=0.0301,
        grain_number=6, #NOTE: 6 GRAIN XL CASE
        grain_density=5121.683939,
        grain_outer_radius=0.04596,
        grain_initial_inner_radius=0.013195,
        grain_initial_height=0.1683173333,
        grain_separation=0.005,
        grains_center_of_mass_position=0.35228,
        center_of_dry_mass_position=0.35228,
        nozzle_position=0.0,
        burn_time=7.04,
        throat_radius=0.013195,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    """
    O3400:
    https://pro38.com44/products/p98-6gxl/21062o3400-p/
    """
    O3400 = SolidMotor(
        thrust_source="./src/motors/Cesaroni_21062O3400-P.eng",
        dry_mass=4.3985,
        dry_inertia=(0.00876,0.8265,0.8265),
        nozzle_radius=0.0301,
        grain_number=6, #NOTE: 6 GRAIN XL CASE
        grain_density=5121.683939,
        grain_outer_radius=0.04596,
        grain_initial_inner_radius=0.013195,
        grain_initial_height=0.1683173333,
        grain_separation=0.005,
        grains_center_of_mass_position=0.35228,
        center_of_dry_mass_position=0.35228,
        nozzle_position=0.0,
        burn_time=6.16,
        throat_radius=0.013195,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )
