import numpy as np

# Goal: design a transmitting loop, with a mag. moment = 50-100 Am^2

# Constants
METER_TO_FEET = 3.28084
FEET_TO_METER = 1 / METER_TO_FEET
LB_TO_KG = 0.453592
RL_18AWG = 20.9 / 1000  # Ohms per km of wire for #18 AWG
WEIGHT_18AWG = 0.010 # lbs/ft

N = 75
I = 1.5  # Peak AC current

width = 2 * FEET_TO_METER # 2 ft loop
height = 2.5 * FEET_TO_METER # 2.5 ft loop

A = width * height  # 2x3 ft loop
f = 30  # frequency that you are driving the loop at. This small signal comes from the Raspberry Pi.
w = 2 * np.pi * f

magnetic_moment = N * I * A  # N is the number of turns, I is the current in the wire, and A is the area of the loop.

perimiter = height * 2 + width * 2

R = perimiter * N * RL_18AWG
perimiter_feet = perimiter * METER_TO_FEET
weight_wire = perimiter_feet * WEIGHT_18AWG * N


# Inductance?
# https://www.allaboutcircuits.com/tools/rectangle-loop-inductance-calculator/

L = 0.00000393 * N**2  # Inductance for N turns, 2x3 loop

Zl = w * L
magZ = np.sqrt(R**2 + Zl**2)

Vp = I * magZ  # Peak voltage that needs to be applied to the loop from the audio amplifier without series capacitor
Vp_c = I * R  # Peak voltage that needs to be applied from the audio amplifier with a series capacitor added

Vpa = 2 * Vp  # DC power amplifier voltage (Max amount we can handle; max amount voltage capacitor can put out)

Cs = 1 / (L * w**2)  # Series capacitance needed to cancel inductance

average_loop_power = 0.5 * I**2 * R


curr_power = np.inf
# Iterate through different combinations of N and I to get the desired magnetic moment and minimize power

"""for n in range(1, 100):
    # Iterate through different currents by 0.5
    for i_mult in range(0, 100, 5):
        i = i_mult / 10
        magnetic_moment = n * i * A
        if magnetic_moment <= 50:
            continue

        R = perimiter * n * rl_18AWG
        P = 0.5 * i**2 * R
        if P < curr_power:
            curr_power = P
            best_N = n
            best_I = i
        

print(f"Best N: {best_N}, Best I: {best_I}, Best Power: {curr_power}, magnetic moment: {best_N * best_I * A}")"""



# Print results
print(f"Magnetic moment (m): {magnetic_moment:.2f} Am^2")
print(f"Resistance (R): {R:.6f} Ohms")
print(f"Inductance (L): {L:.6f} H")
print(f"Impedance magnitude (|Z|): {magZ:.6f} Ohms")
print(f"Peak voltage without capacitor (Vp): {Vp:.2f} V")
print(f"Peak voltage with capacitor (Vp_c): {Vp_c:.2f} V")
print(f"DC power amplifier voltage (Vpa): {Vpa:.2f} V")
print(f"Series capacitance (Cs): {Cs:.6f} F")
print(f"Power (P): {average_loop_power:.2f} W")
print(f"Total Wire needed (ft): {perimiter_feet*N:.2f} ft") 
print(f"Total Weight of Wire (kg): {weight_wire:.2f} lb")
