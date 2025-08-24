from rocketpy import Environment, SolidMotor, Rocket, Flight
import datetime

#Using info from Caltech's AJAKS rocket to learn rocketpy for 2 stages



### 1. Environment Setup

env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

env.set_date(
    (tomorrow.year, tomorrow.month, tomorrow.day, 12)
)  # Hour given in UTC time

env.set_atmospheric_model(type="Forecast", file="GFS")
env.max_expected_height = 8000

### 2. Stage 1 Definition

Pro75M1670 = SolidMotor(
    thrust_source="./Cesaroni_6026M1670-P.eng",
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

# 14.426 is the mass of the rocket including the payload but without the motor
payload_mass = 4.5  # in kg
rocket_mass = 14.426 - payload_mass  # in kg


stage1_rocket = Rocket(
    radius=127 / 2000,
    mass=rocket_mass + rocket_mass,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag="./powerOffDragCurve.csv",
    power_on_drag="./powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

stage1_rocket.add_motor(Pro75M1670, position=-1.255)

stage1_rocket.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.618,
    angular_position=45,
)

stage1_rocket.add_nose(length=0.55829, kind="von karman", position=1.278)

stage1_rocket.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    position=-1.04956,
    cant_angle=0.5,
)

stage1_rocket.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)

"""#lower stage 1 fins
fins = rocket.addTrapezoidalFins(
    n=4,
    rootChord=0.25,       # [m] from figure
    tipChord=0.10,        # [m]
    span=0.15,            # [m]
    distanceToCM=-0.5     # [m] fin root LE to CM
)

#upper stage 2 fins!
fins = rocket.addTrapezoidalFins(
    n=4,
    rootChord=0.25,       # [m] from figure
    tipChord=0.10,        # [m]
    span=0.15,            # [m]
    distanceToCM=-0.5     # [m] fin root LE to CM
)
"""
stage1_flight = Flight(
    rocket=stage1_rocket,
    environment=env,
    rail_length=5.2,
    inclination=85,
    heading=25,
    terminate_on_apogee=True,
    name="stage1_flight",
)




### 2. Stage 2 Definition

stage2_rocket = Rocket(
    radius=127 / 2000,
    mass=rocket_mass,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag="./powerOffDragCurve.csv",
    power_on_drag="./powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

Pro75M1670upper = SolidMotor(
    thrust_source="./Cesaroni_6026M1670-P.eng",
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

stage2_rocket.add_motor(Pro75M1670upper, position=-1.255)



new_sol = stage1_flight.solution[-1]
new_sol[0] = 2.0

print("initial solution:\n")
for i in new_sol:
    print(i)


stage2_flight = Flight(
    rocket=stage2_rocket,
    environment=env,
    rail_length=5.2,  # does not matter since the flight is starting at apogee
    inclination=0,
    heading=0,
    initial_solution=new_sol,
    name="stage2_flight",
)

stage2_flight.all_info()


from rocketpy.plots.compare import CompareFlights

comparison = CompareFlights(
    #[flight_with_payload, flight_without_payload, payload_flight]
    [stage1_flight, stage2_flight]
)

comparison.trajectories_3d(legend=True)