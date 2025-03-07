# This will be used as a psuedo simulation of the power usage of all of the components on the boat.
# This will be used to determine the power requirements of the boat and the battery capacity needed, along with solar

# If we only use the most conservative values it doesn't get close to the power we have available
# At minimum, I think the Rpi should be on 24/7, but hopefully we can put it into a low power mode when not in heavy use. 
# Also, if we do a setup where the boat is stationary and only the sensors are on, we may run into issues where the waves would 
# cause the boat to move and it'd require more power to get back to the original location and heading. 

import numpy as np
from transmission_loop import average_loop_power
# List to store parts
parts = [
    # TODO: Need to properly estimate the power usage and percentage on for each part
    # The Rpi, Servo, Sensors, and Flight controller need to be updated with more accurate values.
    # The power_use is the peak power usage without accounting for time on

    {'name': 'Propulsion motor', 'percentage_on': 15, 'power_use': 60},
    {'name': 'Transmission loop', 'percentage_on': 100, 'power_use': average_loop_power},
    {'name': 'Raspberry Pi', 'percentage_on': 100, 'power_use': 5},
    {'name': 'Servo', 'percentage_on': 1, 'power_use': 10},   # Update Servo power usage and estimation of percentage on
    {'name': 'Sensors', 'percentage_on': 100, 'power_use': 5},
    {'name': 'Flight Controller', 'percentage_on': 100, 'power_use': 6} #See if we can find a good estimate for this, estimating the same as the Pi
    # Add more parts as needed
]

# PV power potential taken from https://globalsolaratlas.info/download/vietnam, conservatively using 4 as offshore doesn't have to deal with terrain, but confirm with client 
# what part of vietnam the boat would be

PV_power_potential = 4 # kWh/kWp/day, multiply this by our panel wattage to get an estimate of the power we can get from the sun
operating_hours = 24 # Hours, how long the boat will be operating for. See if we can calculate this based on the time needed to travel the 81 square miles and the speed of the boat. 
using_solar = True

solar_panel_wattage = 100 # Watts
CELL_VOLTAGE = 3.7 # Volts

#Battery Specs
twoS_battery_dict = {'S rating': 2, 'Capacity': 38.38, 'C rating': 50}
# Need to find 3S battery specs if we are using the SpeedyBee V4, which takes a 3-6S battery

dict_list = [twoS_battery_dict]
for dictionary in dict_list:
    print(f"Calculating battery specs for {dictionary['S rating']}S battery")
    battery_voltage = CELL_VOLTAGE * dictionary['S rating'] # 2S battery
    battery_capacity_Wh = dictionary['Capacity'] # Wh
    battery_capacity_Ah = battery_capacity_Wh / battery_voltage # Ah
    battery_max_discharge_rating = dictionary['C rating'] # Unitless
    battery_max_discharge_A = battery_max_discharge_rating * battery_capacity_Ah # A

    print(f"    Battery capacity: {battery_capacity_Ah:.2f}Ah, {battery_capacity_Wh:.2f}Wh")
    print(f"    Maximum discharge: {battery_max_discharge_A:.2f}A")

# Calculate the total power usage
total_power_usage = 0
peak_power_usage = 0

print("Power usage by part:")
for part in parts:
    print(f"    Part: {part['name']}, Percentage On: {part['percentage_on']}%, Power Use: {part['power_use']:.2f}W")
    total_power_usage += part['power_use'] * part['percentage_on'] / 100
    peak_power_usage += part['power_use']

daily_energy_usage = total_power_usage * operating_hours # Wh
energy_generated_per_day = solar_panel_wattage * PV_power_potential if using_solar else 0

print(f"Average power: {total_power_usage:.2f}W")
print(f"Peak power: {peak_power_usage:.2f}W")
print(f"Energy used per day: {daily_energy_usage:.2f}Wh")
print(f"Energy generated per day: {energy_generated_per_day:.2f}Wh")

# Need this to be true for fully autonomous system
print(f"System is autonomous: {energy_generated_per_day > daily_energy_usage}")

# TODO: Check if the battery capacity is enough, and the peak output power is enough