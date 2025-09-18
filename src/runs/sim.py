from rocketpy import Flight
#TODO: import desvars, missionreqs
from src.models.env import build_env
from src.utils.build_config import build_config
from src.utils.build_rocket import build_rocket
from src.models.aero_bending import aero_bending

# Atmosphere and launch environment
def flightsim(desvars, missionreqs):
    env = build_env()
    config = build_config(desvars, missionreqs)

    # Build rocket from design vars
    rocket, mm = build_rocket(config)

    # Run a flight
    flight = Flight(
        rocket=rocket,
        environment=env,
        rail_length=missionreqs.rail_length,
        inclination=85,
        heading=0
    )

    #TODO:
    # Check Aero Loads Constraint
    #aero_bending("""MAX Q LOADS FROM RKTPY""")

    return 1
