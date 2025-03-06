
# This will be used as a psuedo simulation of the power usage of all of the components on the boat.
# This will be used to determine the power requirements of the boat and the battery capacity needed, along with solar

import numpy as np


# Constants
METER_TO_FEET = 3.28084
FEET_TO_METER = 1 / METER_TO_FEET
using_solar = True


# GHI taken from https://globalsolaratlas.info/download/vietnam, conservatively using 4 as offshore doesn't have to deal with terrain, but confirm with client 
# what part of vietnam the boat would be

PV_power_potential = 4 # kWh/kWp/day, multiply this by our panel wattage to get an estimate of the power we can get from the sun
operating_hours = 4 # Hours, how long the boat will be operating for. See if we can calculate this based on the time needed to travel the 81 square miles. 

# List to store parts
parts = [
    {'name': 'Propulsion motor', 'percentage_on': 100, 'power_use': 60},
    {'name': 'Raspberry Pi', 'percentage_on': 100, 'power_use': 6},
    {'name': 'Servo', 'percentage_on': 10, 'power_use': 10},   # Update Servo power usage and estimation of percentage on
    {'name': 'Sensors', 'percentage_on': 100, 'power_use': 5},
    {'name': 'Flight Controller', 'percentage_on': 100, 'power_use': 6} #See if we can find a good estimate for this, estimating the same as the Pi
    # Add more parts as needed
]

solar_panel_wattage = 100 # Watts
battery_capacity = 100 # Ah

# Calculate the total power usage
total_power_usage = 0
# Example of how to access the data
for part in parts:
    print(f"Part: {part['name']}, Percentage On: {part['percentage_on']}%, Power Use: {part['power_use']}W")
    total_power_usage += part['power_use'] * part['percentage_on'] / 100

daily_power_usage = total_power_usage * operating_hours # Wh
energy_generated_per_day = solar_panel_wattage * PV_power_potential

print(f"Total power usage: {total_power_usage}W, Daily power usage: {daily_power_usage}Wh")
print(f"Energy generated per day: {energy_generated_per_day}Wh")

