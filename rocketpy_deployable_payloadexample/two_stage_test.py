# -*- coding: utf-8 -*-
"""
Created on 10/13/2020
@author: Dyllon Preston
Make sure you update the file directories to match your files!
"""

from rocketpy import Environment, Rocket, SolidMotor, Flight
import math

# Parameters for environment for rocket stage 1
Env1 = Environment(
    #railLength=10,
    latitude=32.990254,
    longitude=-106.974998,
    elevation=1400, #the elevation for stage 1 would be the distance above sea level
    date=(2020, 9, 21, 12) # Tomorrow's date in year, month, day, hour UTC format
) 

# Parameters for first stage motor
motor1 = SolidMotor(
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

# Parameters for first stage rocket
rocket_stage1 = Rocket(
    radius=127 / 2000,
    mass=10,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag="./powerOffDragCurve.csv",
    power_on_drag="./powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose"
)

rocket_stage1.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.618,
    angular_position=45,
)

# Parameters for first stage nose cone
NoseCone = rocket_stage1.add_nose(length=0.78359, kind="vonKarman", position=1.278)

# Parameters for first stage fins
FinSet = rocket_stage1.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    position=-1.04956,
    cant_angle=0.5,
)
# Parameters for first stage tail
# Tail = rocket_stage1.addTail(topRadius=0.0635, bottomRadius=0.0435, length=0.060, distanceToCM=-1.194656)

# Defining triggers for parachutes
def drogueTrigger(p, y):
    return True if y[5] < 0 else False

def mainTrigger(p, y):
    return True if y[5] < 0 and y[2] < 800 else False

"""# Parameters for first stage main parachute
Main = rocket_stage1.add_parachute(
    "Main",
    cd_s=7.2,
    trigger=800,
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)"""

"""# Parameters for first stage drogue
Drogue = rocket_stage1.add_parachute(
    "Drogue",
    cd_s=0.72,
    trigger="apogee",
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)"""

# Parameters for first stage rocket flight
Flight_stage1 = Flight(rocket=rocket_stage1, environment=Env1, rail_length=5.2, inclination=85, heading=0 ,verbose=True)

# Post processing of first stage

"""
#//////////////////////////////////////////////             Rocket  Stage 2             //////////////////////////////////////////////////////////////////////////////////////#
"""

# Ignition delay between stage 1 and stage 2
ignition_delay = 4
tsecond_stage = motor1.burn_out_time + ignition_delay

# Parameters for second stage environment
Env2 = Environment(
    latitude= Env1.latitude + (Flight_stage1.y(tsecond_stage) / 6378000) * (180 / math.pi),
    longitude= Env1.longitude + (Flight_stage1.x(tsecond_stage) / 6378000) * (180 / math.pi) / (math.cos(Env1.latitude * math.pi / 180)),
    elevation=Flight_stage1.z(tsecond_stage), # elevation must be updated to avoid a discontinuity
    date=(2020, 9, 21, 12) # Tomorrow's date in year, month, day, hour UTC format
) 

# Parameters for second stage motor
motor2 = motor1

# Parameters for the second stage rocket
rocket_stage2 = rocket_stage1


# Parameters for second stage main parachute
"""Main = rocket_stage2.add_parachute(
    "Main",
    cd_s=7.2,
    trigger=800,
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)"""

# Parameters for the second stage drogue
"""Drogue = rocket_stage2.add_parachute(
    "Drogue",
    cd_s=0.72,
    trigger=None,
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)"""

# Parameters for the second stage flight
Flight_stage2 = Flight(rocket=rocket_stage2, environment=Env2, inclination=Flight_stage1.w1(tsecond_stage), rail_length=5.2, heading=0, initial_solution=Flight_stage1 ) #[0, Flight_stage1.x(tsecond_stage), 0, Flight_stage1.z(tsecond_stage), Flight_stage1.vx(tsecond_stage), Flight_stage1.vy(tsecond_stage), 0, Flight_stage1.e0(tsecond_stage), Flight_stage1.e1(tsecond_stage), Flight_stage1.e2(tsecond_stage), Flight_stage1.e3(tsecond_stage), Flight_stage1.w1(tsecond_stage), Flight_stage1.w2(tsecond_stage), Flight_stage1.w3(tsecond_stage)])

# Post processing of the second stage
from rocketpy.plots.compare import CompareFlights

comparison = CompareFlights(
    [Flight_stage1, Flight_stage2]
)

"""
#//////////////////////////////////////////////             Print Data             //////////////////////////////////////////////////////////////////////////////////////#
"""

# Prints all graphs for stage 1
# Flight_stage1.allInfo()

#Prints all graphs for stage 2
#Flight_stage2.all_info()