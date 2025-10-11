from uvicrocketpy import Environment, SolidMotor, Rocket, Flight

import numpy as np

# 1. Environment
env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)
# set date, atmosphere etc. …
env.set_date((2025, 10, 10, 18))
env.set_atmospheric_model(type="Forecast", file="GFS")

def Cd_power_off(Mach, altitude):

    print("confirm ma, alt: ", Mach, altitude)

    # Compressibility correction + density scaling
    Cd0 = 0.3 + 0.1 * np.exp(-altitude / 8000)
    compressibility = 1 + 0.25 * (Mach - 1)**2 if Mach > 1 else 1
    return Cd0 * compressibility



# 2. Rocket
calisto = Rocket(
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag=Cd_power_off,
    power_on_drag=Cd_power_off,
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

Pro75M1670 = SolidMotor(
    thrust_source="engine.eng",
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


calisto.add_motor(Pro75M1670, position=-1.255)


rail_buttons = calisto.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.6182,
    angular_position=45,
)

nose_cone = calisto.add_nose(
    length=0.55829, kind="von karman", position=1.278
)

fin_set = calisto.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    position=-1.04956,
    cant_angle=0.5,
    airfoil=("NACA0012-radians.txt","radians"),
)

tail = calisto.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)

# 3. Simulate
test_flight = Flight(
    rocket=calisto,
    environment=env,
    rail_length=5.2,
    inclination=85,
    heading=0
)

# 4. Analyze
test_flight.all_info()
test_flight.speed.plot(0, test_flight.apogee_time)
