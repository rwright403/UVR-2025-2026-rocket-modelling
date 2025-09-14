from enum import Enum
from rocketpy import SolidMotor

### NOTE: THIS IS ALL VIBE CODE BOILERPLATE
### TODO: REPLACE WITH REAL VALUES!

class Motor(Enum):
    M1790 = SolidMotor(
        thrust_source="./motors/8088M1790-P.eng",
        dry_mass=None,
        dry_inertia=None,
        nozzle_radius=None,
        grain_number=4,
        grain_density=None,
        grain_outer_radius=None,
        grain_initial_inner_radius=None,
        grain_initial_height=None,
        grain_separation=None,
        grains_center_of_mass_position=None,
        center_of_dry_mass_position=None,
        nozzle_position=None,
        burn_time=None,
        throat_radius=None,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    M1450 = SolidMotor(
        thrust_source="./motors/9955M1450-P.eng",
        dry_mass=None,
        dry_inertia=None,
        nozzle_radius=None,
        grain_number=4,
        grain_density=None,
        grain_outer_radius=None,
        grain_initial_inner_radius=None,
        grain_initial_height=None,
        grain_separation=None,
        grains_center_of_mass_position=None,
        center_of_dry_mass_position=None,
        nozzle_position=None,
        burn_time=None,
        throat_radius=None,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    M3400 = SolidMotor(
        thrust_source="./motors/9994M3400-P.eng",
        dry_mass=None,
        dry_inertia=None,
        nozzle_radius=None,
        grain_number=4,
        grain_density=None,
        grain_outer_radius=None,
        grain_initial_inner_radius=None,
        grain_initial_height=None,
        grain_separation=None,
        grains_center_of_mass_position=None,
        center_of_dry_mass_position=None,
        nozzle_position=None,
        burn_time=None,
        throat_radius=None,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    M795 = SolidMotor(
        thrust_source="./motors/10133M795-P.eng",
        dry_mass=None,
        dry_inertia=None,
        nozzle_radius=None,
        grain_number=4,
        grain_density=None,
        grain_outer_radius=None,
        grain_initial_inner_radius=None,
        grain_initial_height=None,
        grain_separation=None,
        grains_center_of_mass_position=None,
        center_of_dry_mass_position=None,
        nozzle_position=None,
        burn_time=None,
        throat_radius=None,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    N3400 = SolidMotor(
        thrust_source="./motors/14263N3400-P.eng",
        dry_mass=None,
        dry_inertia=None,
        nozzle_radius=None,
        grain_number=6,
        grain_density=None,
        grain_outer_radius=None,
        grain_initial_inner_radius=None,
        grain_initial_height=None,
        grain_separation=None,
        grains_center_of_mass_position=None,
        center_of_dry_mass_position=None,
        nozzle_position=None,
        burn_time=None,
        throat_radius=None,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    N2540 = SolidMotor(
        thrust_source="./motors/17907N2540-P.eng",
        dry_mass=None,
        dry_inertia=None,
        nozzle_radius=None,
        grain_number=6,
        grain_density=None,
        grain_outer_radius=None,
        grain_initial_inner_radius=None,
        grain_initial_height=None,
        grain_separation=None,
        grains_center_of_mass_position=None,
        center_of_dry_mass_position=None,
        nozzle_position=None,
        burn_time=None,
        throat_radius=None,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    O3400 = SolidMotor(
        thrust_source="./motors/21062O3400-P.eng",
        dry_mass=None,
        dry_inertia=None,
        nozzle_radius=None,
        grain_number=6,
        grain_density=None,
        grain_outer_radius=None,
        grain_initial_inner_radius=None,
        grain_initial_height=None,
        grain_separation=None,
        grains_center_of_mass_position=None,
        center_of_dry_mass_position=None,
        nozzle_position=None,
        burn_time=None,
        throat_radius=None,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )
