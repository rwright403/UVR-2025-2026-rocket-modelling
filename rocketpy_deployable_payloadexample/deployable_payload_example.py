from rocketpy import Environment, SolidMotor, Rocket, Flight

env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)

import datetime

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

env.set_date(
    (tomorrow.year, tomorrow.month, tomorrow.day, 12)
)  # Hour given in UTC time

env.set_atmospheric_model(type="Forecast", file="GFS")
env.max_expected_height = 8000

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

print(
    "Rocket Mass Without Motor: {:.4} kg (with Payload)".format(
        rocket_mass + payload_mass
    )
)
print("Loaded Motor Mass: {:.4} kg".format(Pro75M1670.total_mass(0)))
print("Payload Mass: {:.4} kg".format(payload_mass))
print(
    "Fully loaded Rocket Mass: {:.4} kg".format(
        rocket_mass + Pro75M1670.total_mass(0) + payload_mass
    )
)

rocket_with_payload = Rocket(
    radius=127 / 2000,
    mass=rocket_mass + rocket_mass,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag="./powerOffDragCurve.csv",
    power_on_drag="./powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

rocket_with_payload.add_motor(Pro75M1670, position=-1.255)

rocket_with_payload.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.618,
    angular_position=45,
)

rocket_with_payload.add_nose(length=0.55829, kind="von karman", position=1.278)

rocket_with_payload.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    position=-1.04956,
    cant_angle=0.5,
)

rocket_with_payload.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)

rocket_with_payload.info()

flight_with_payload = Flight(
    rocket=rocket_with_payload,
    environment=env,
    rail_length=5.2,
    inclination=85,
    heading=25,
    terminate_on_apogee=True,
    name="Rocket Flight With Payload",
)

rocket_without_payload = Rocket(
    radius=127 / 2000,
    mass=rocket_mass,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag="./powerOffDragCurve.csv",
    power_on_drag="./powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)


# Define Parachutes for the rocket
main_chute = rocket_without_payload.add_parachute(
    "Main",
    cd_s=7.2,
    trigger=800,
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

drogue_chute = rocket_without_payload.add_parachute(
    "Drogue",
    cd_s=0.72,
    trigger="apogee",
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

flight_without_payload = Flight(
    rocket=rocket_without_payload,
    environment=env,
    rail_length=5.2,  # does not matter since the flight is starting at apogee
    inclination=0,
    heading=0,
    initial_solution=flight_with_payload,
    name="Rocket Flight Without Payload",
)

# Define the "Payload Rocket"

payload_rocket = Rocket(
    radius=127 / 2000,
    mass=payload_mass,
    inertia=(0.1, 0.1, 0.001),
    power_off_drag=0.5,
    power_on_drag=0.5,
    center_of_mass_without_motor=0,
)

payload_drogue = payload_rocket.add_parachute(
    "Drogue",
    cd_s=0.35,
    trigger="apogee",
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

payload_main = payload_rocket.add_parachute(
    "Main",
    cd_s=4.0,
    trigger=800,
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

payload_flight = Flight(
    rocket=payload_rocket,
    environment=env,
    rail_length=5.2,  # does not matter since the flight is starting at apogee
    inclination=0,
    heading=0,
    initial_solution=flight_with_payload,
    name="PayloadFlight",
)

from rocketpy.plots.compare import CompareFlights

comparison = CompareFlights(
    [flight_with_payload, flight_without_payload, payload_flight]
)

comparison.trajectories_3d(legend=True)