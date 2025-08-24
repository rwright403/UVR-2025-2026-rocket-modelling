import numpy as np
from rocketpy import Environment, SolidMotor, Flight
from rocketpy.plots.compare import CompareFlights
from utils.two_stage import TwoStageRocket, mass


env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)
env.set_date((2025, 1, 1, 12))
env.set_atmospheric_model(type="standard_atmosphere")
env.wind_speed = 0

# motors
s1_motor = SolidMotor(
    thrust_source="../rocketpy_deployable_payloadexample/Cesaroni_6026M1670-P.eng",
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=33 / 1000,
    grain_number=5,
    grain_density=1815,
    grain_outer_radius=33 / 1000,
    grain_initial_inner_radius=15 / 1000,
    grain_initial_height=120 / 1000,
    grain_separation=5 / 1000,
    grains_center_of_mass_position=0.397,
    center_of_dry_mass_position=0.317,
    nozzle_position=0,
    burn_time=3.9,
    throat_radius=11 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)
s2_motor = SolidMotor(
    thrust_source="../rocketpy_deployable_payloadexample/Cesaroni_6026M1670-P.eng",
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=33 / 1000,
    grain_number=5,
    grain_density=1815,
    grain_outer_radius=33 / 1000,
    grain_initial_inner_radius=15 / 1000,
    grain_initial_height=120 / 1000,
    grain_separation=5 / 1000,
    grains_center_of_mass_position=0.397,
    center_of_dry_mass_position=0.317,
    nozzle_position=0,
    burn_time=3.9,
    throat_radius=11 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

# placeholder drag models
class DummyDrag:
    power_off = "../rocketpy_deployable_payloadexample/powerOffDragCurve.csv"
    power_on = "../rocketpy_deployable_payloadexample/powerOnDragCurve.csv"

# placeholder mass models
dummy_mass = mass.mass(40, [2.4,0,0], np.diag([2.3, 2.3, 0.03]) )

s1_mass = dummy_mass
s2_mass = dummy_mass

# build the two-stage rocket
rocket = TwoStageRocket(
    s1_rail_buttons=(3.3, 3.8, 45),
    s1_diam=0.2032,
    s1_motor_x_pos=5.0,
    s1_motor=lambda r, pos: r.add_motor(s1_motor, position=pos),
    s1_fins_x_pos=5.0,
    s1_fins=lambda r, pos: r.add_trapezoidal_fins(n=4, root_chord=0.25, tip_chord=0.1, span=0.1, position=pos),
    s1_boattail_x_pos=2.6,
    s1_boattail=lambda r, pos: r.add_tail(top_radius=0.076, bottom_radius=0.102, length=0.175, position=pos),
    s1_mass_model=s1_mass,
    s1_separated_drag_model=DummyDrag,
    s1_drogue= None,
    s1_main= None, 

    full_stack_length=5.0,
    full_stack_drag_model=DummyDrag,

    s2_length=3.0,
    s2_diam=0.2032,
    s2_motor_x_pos=2.6,
    s2_motor=lambda r, pos: r.add_motor(s2_motor, position=pos),
    s2_fins_x_pos=2.2,
    s2_fins=lambda r, pos: r.add_trapezoidal_fins(n=3, root_chord=0.25, tip_chord=0.1, span=0.1, position=pos),
    s2_boattail_x_pos=2.5,
    s2_boattail=None,  # not needed
    s2_mass_model=s2_mass,
    s2_drag_model=DummyDrag,
    s2_drogue=None,
    s2_main=None,
    nosecone=lambda r, pos: r.add_nose(length=0.3, kind="von karman", position=pos)
)

# run flights
stage1_flight = Flight(rocket=rocket.full_stack, environment=env, rail_length=20.0, inclination=89, heading=0)
#stage2_init = stage1_flight.get_solution_at_time(3.0, atol=0.001)
#stage2_flight = Flight(rocket=rocket.stage2, environment=env, initial_solution=stage2_init, rail_length=0.1, inclination=89, heading=0)


stage1_flight.all_info()
#CompareFlights([stage1_flight, stage2_flight]).trajectories_3d(legend=True)
