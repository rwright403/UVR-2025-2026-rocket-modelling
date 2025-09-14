from rocketpy import Flight
#TODO: import desvars, missionreqs
from src.models.env import build_env
from src.utils.build_rocket import build_rocket
from src.models.aero_bending import aero_bending

# Atmosphere and launch environment
env = build_env()

# Build rocket from design vars
rocket = build_rocket(desvars, missionreqs)

# Run a flight
flight = Flight(
    rocket=rocket,
    environment=env,
    inclination=85,
    heading=0
)

#TODO:
# Check Aero Loads Constraint
#aero_bending("""MAX Q LOADS FROM RKTPY""")
