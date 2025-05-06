import numpy as np
from transmission_loop import average_loop_power

# List to store parts
parts = [
    # TODO: Need to properly estimate the power usage and percentage on for each part
    # The Rpi, Servo, Sensors, and Flight controller need to be updated with more accurate values.
    # The power_use is the peak power usage without accounting for time on
    {'name': 'Propulsion motor', 'percentage_on': 15, 'power_use': 60},
    {'name': 'Transmission loop', 'percentage_on': 100, 'power_use': average_loop_power},
    {'name': 'Raspberry Pi', 'percentage_on': 100, 'power_use': 4},
    {'name': 'Servo', 'percentage_on': 10, 'power_use': 10},   # Update Servo power usage and estimation of percentage on
    {'name': 'Sensors', 'percentage_on': 100, 'power_use': 1},
    {'name': 'Flight Controller', 'percentage_on': 100, 'power_use': 4} # Estimating same as the Pi
    # Add more parts as needed
]

# PV power potential taken from https://globalsolaratlas.info/download/vietnam, 
# conservatively using 4 as offshore doesn't have to deal with terrain, but confirm with client 
# what part of vietnam the boat would be.
PV_power_potential = 4  # kWh/kWp/day; multiplied by our panel wattage gives an estimate of available solar energy
operating_hours = 24    # Hours, how long the boat will be operating for
using_solar = True

solar_panel_wattage = 60  # Watts. 55W is around the minimum for an autonomous system
CELL_VOLTAGE = 3.7         # Volts

# Battery Specs
twoS_battery_dict = {'S rating': 2, 'Capacity': 38.38, 'C rating': 50}
# Need to find 3S battery specs if using the SpeedyBee V4, which takes a 3-6S battery

dict_list = [twoS_battery_dict]
for dictionary in dict_list:
    print(f"Calculating battery specs for {dictionary['S rating']}S battery")
    battery_voltage = CELL_VOLTAGE * dictionary['S rating']  # e.g. 2S battery
    battery_capacity_Wh = dictionary['Capacity']             # Wh
    battery_capacity_Ah = battery_capacity_Wh / battery_voltage  # Ah
    battery_max_discharge_rating = dictionary['C rating']      # Unitless
    battery_max_discharge_A = battery_max_discharge_rating * battery_capacity_Ah  # A

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

daily_energy_usage = total_power_usage * operating_hours  # Wh
energy_generated_per_day = solar_panel_wattage * PV_power_potential if using_solar else 0

print(f"Average power: {total_power_usage:.2f}W")
print(f"Peak power: {peak_power_usage:.2f}W")
print(f"Energy used per day: {daily_energy_usage:.2f}Wh")
print(f"Energy generated per day: {energy_generated_per_day:.2f}Wh")
print(f"System is autonomous: {energy_generated_per_day > daily_energy_usage}")

# Assume battery capacity is as calculated from specs or set to a specific value for simulation.
battery_capacity_Wh = 2*12.8*8

def simulate_days(days, operating_hours=24):
    simulation_duration_seconds = days * operating_hours * 3600  # N days in seconds
    battery_energy = battery_capacity_Wh  # Wh; start fully charged

    energy_usage_per_sec = total_power_usage / 3600.0  # Wh per second
    solar_energy_per_sec = solar_panel_wattage / 3600.0  # Wh per second

    print(f"Starting {days}-day simulation (second-by-second)...")
    
    for t in range(simulation_duration_seconds):
        current_hour = (t / 3600.0) % 24  # current hour of the day (resets every 24 hours)

        battery_energy -= energy_usage_per_sec

        if battery_energy < 0:
            print(f"Time {t / 3600.0:.2f}h: Battery depleted. System is not autonomous.")
            return

        # Solar charging occurs from 10:00 to 14:00 every day
        if 0 <= (current_hour % operating_hours) < PV_power_potential and using_solar:   # Assuming 10am to 2pm for 100% solar, 
            battery_energy += solar_energy_per_sec
            battery_energy = min(battery_energy, battery_capacity_Wh)

        if t % 3600 == 0:
            print(f"Time {t / 3600.0:.2f}h: Battery energy: {battery_energy:.2f}Wh")
    
    print("Simulation complete.")
    if battery_energy >= 0:
        print("System remains autonomous after the simulation period.")
    else:
        print("System is not autonomous after the simulation period.")

simulate_days(10, 8)  # Simulate 8 hours for 5 days
