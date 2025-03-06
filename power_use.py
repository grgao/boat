
# This will be used as a psuedo simulation of the power usage of all of the components on the boat.
# This will be used to determine the power requirements of the boat and the battery capacity needed, along with solar

# If we only use the most conservative values it doesn't get close to the power we have available
# At minimum, I think the Rpi should be on 24/7, but hopefully we can put it into a low power mode when not in heavy use. 
# Also, if we do a setup where the boat is stationary and only the sensors are on, we may run into issues where the waves would 
# cause the boat to move and it'd require more power to get back to the original location and heading. 

import numpy as np


# Constants
METER_TO_FEET = 3.28084
FEET_TO_METER = 1 / METER_TO_FEET
using_solar = True


# PV power potential taken from https://globalsolaratlas.info/download/vietnam, conservatively using 4 as offshore doesn't have to deal with terrain, but confirm with client 
# what part of vietnam the boat would be

PV_power_potential = 4 # kWh/kWp/day, multiply this by our panel wattage to get an estimate of the power we can get from the sun
operating_hours = 24 # Hours, how long the boat will be operating for. See if we can calculate this based on the time needed to travel the 81 square miles and the speed of the boat. 

# List to store parts
parts = [
    # TODO: Need to properly estimate the power usage and percentage on for each part
    # The Rpi, Servo, Sensors, and Flight controller need to be updated with more accurate values.

    {'name': 'Propulsion motor', 'percentage_on': 15, 'power_use': 60},
    {'name': 'Raspberry Pi', 'percentage_on': 100, 'power_use': 5},
    {'name': 'Servo', 'percentage_on': 1, 'power_use': 10},   # Update Servo power usage and estimation of percentage on
    {'name': 'Sensors', 'percentage_on': 100, 'power_use': 5},
    {'name': 'Flight Controller', 'percentage_on': 100, 'power_use': 6} #See if we can find a good estimate for this, estimating the same as the Pi
    # Add more parts as needed
]

solar_panel_wattage = 100 # Watts
battery_capacity = 100 # Ah

one_cell_voltage = 3.7 # Volts
battery_voltage = one_cell_voltage * 3 # 3S battery, need to purchase one


# Calculate the total power usage
total_power_usage = 0
peak_power_usage = 0

for part in parts:
    print(f"Part: {part['name']}, Percentage On: {part['percentage_on']}%, Power Use: {part['power_use']}W")
    total_power_usage += part['power_use'] * part['percentage_on'] / 100
    peak_power_usage += part['power_use']

print("")

daily_energy_usage = total_power_usage * operating_hours # Wh
energy_generated_per_day = solar_panel_wattage * PV_power_potential if using_solar else 0

print(f"Average power: {total_power_usage}W")
print(f"Energy used per day: {daily_energy_usage:.2f}Wh")
print(f"Peak power: {peak_power_usage}W")
print(f"Energy generated per day: {energy_generated_per_day}Wh")

# Need this to be true for fully autonomous system
print(f"System is autonomous: {energy_generated_per_day > daily_energy_usage}")

# TODO: Check if the battery capacity is enough, and the peak output power is enough
