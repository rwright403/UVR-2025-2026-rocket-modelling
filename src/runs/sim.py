from rocketpy import Flight
from src._config.test_config import desvars
from src.models.env import build_env
from src.utils.build_rocket import build_rocket
from src.models.aero_bending import aero_bending

# Atmosphere and launch environment
env = build_env()

# Build rocket from design vars
rocket = build_rocket(desvars)

# Run a flight
flight = Flight(
    rocket=rocket,
    environment=env,
    inclination=85,
    heading=0
)

#TODO:
#aero_bending()



# Inspect results
print("Apogee:", flight.apogee)
print("Max velocity:", flight.max_velocity)

#TODO: PULL OUT MAX Q
