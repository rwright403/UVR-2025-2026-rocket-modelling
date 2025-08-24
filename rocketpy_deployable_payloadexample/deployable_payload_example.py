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
    radius=0.1016,
    mass=rocket_mass + rocket_mass,
    inertia=(2.321, 2.321, 0.034),
    power_off_drag="./powerOffDragCurve.csv",
    power_on_drag="./powerOnDragCurve.csv",
    center_of_mass_without_motor=2.42824,
    coordinate_system_orientation="nose_to_tail",
)

#NOTE: 1 N2000w PARALLEL WITH 2 J350W SOLIDS MOTORS

stage1_rocket.add_motor(Pro75M1670, position=5.03174)

stage1_rocket.set_rail_buttons(
    upper_button_position=3.302,
    lower_button_position=3.81,
    angular_position=45,
)

stage1_rocket.add_nose(length=0.3048, kind="von karman", position=0)


stage1_rocket.add_tail(
    top_radius=0.0762, bottom_radius=0.1016, length=0.17526, position=2.6035
)

#lower stage 1 fins
stage1_rocket.add_trapezoidal_fins(
    n=5,
    root_chord=0.25,       # [m] from figure
    tip_chord=0.10,        # [m]
    span=0.15,            # [m]
    position=3.9243     # [m] fin root LE to CM
)

#upper stage 2 fins!
stage1_rocket.add_trapezoidal_fins(
    n=5,
    root_chord=0.25,       # [m] from figure
    tip_chord=0.10,        # [m]
    span=0.15,            # [m]
    position=2.25     # [m] fin root LE to CM
)


stage1_rocket.draw()

stage1_flight = Flight(
    rocket=stage1_rocket,
    environment=env,
    rail_length=10.2,
    inclination=85,
    heading=25,
    terminate_on_apogee=True,
    name="stage1_flight",
)


print("here")

### 2. Stage 2 Definition

stage2_rocket = Rocket(
    radius=127 / 2000,
    mass=rocket_mass,
    inertia=(2.321, 2.321, 0.034),
    power_off_drag="./powerOffDragCurve.csv",
    power_on_drag="./powerOnDragCurve.csv",
    center_of_mass_without_motor=1.21412,
    coordinate_system_orientation="nose_to_tail",
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

stage2_rocket.add_motor(Pro75M1670upper, position=2.6035)

stage2_rocket.add_trapezoidal_fins(
    n=5,
    root_chord=0.25,       # [m] from figure
    tip_chord=0.10,        # [m]
    span=0.15,            # [m]
    position=2.25     # [m] fin root LE to CM
)


stage2_rocket.add_nose(length=0.3048, kind="von karman", position=0)

stage2_rocket.draw()


### sim
# sol vector: [t, x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
new_sol = stage1_flight.solution[-1]
new_sol[0] = 2.0 #reset initial time
new_sol[7:11] = [1.0, 0.0, 0.0, 0.0]  # e0, e1, e2, e3

print("initial solution:\n")
for i in new_sol:
    print(i)


stage2_flight = Flight(
    rocket=stage2_rocket,
    environment=env,
    rail_length=.1,  # in theory does not matter since the flight is starting at apogee
    inclination=85,
    heading=0,
    initial_solution=new_sol,
    name="stage2_flight",
)

#stage2_flight.all_info()


from rocketpy.plots.compare import CompareFlights

comparison = CompareFlights(
    #[flight_with_payload, flight_without_payload, payload_flight]
    [stage1_flight, stage2_flight]
)

comparison.trajectories_3d(legend=True)