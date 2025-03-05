import numpy as np

# Goal: design a transmitting loop, with a mag. moment = 50-100 Am^2

N = 50
I = 1  # Peak AC current
A = 0.91 * 0.61  # 2x3 ft loop
f = 30  # frequency that you are driving the loop at. This small signal comes from the Raspberry Pi.
w = 2 * np.pi * f

m = N * I * A  # N is the number of turns, I is the current in the wire, and A is the area of the loop.

METER_TO_FEET = 3.28084

rl = 20.9 / 1000  # Ohms per meter of wire for #18 AWG

perimiter = 0.91 * 2 + 0.61 * 2
R = (perimiter) * N * rl

perimiter_feet = perimiter * METER_TO_FEET

# Inductance?
# https://www.allaboutcircuits.com/tools/rectangle-loop-inductance-calculator/

L = 0.00000393 * N**2  # Inductance for N turns, 2x3 loop

Zl = w * L
magZ = np.sqrt(R**2 + Zl**2)

Vp = I * magZ  # Peak voltage that needs to be applied to the loop from the audio amplifier without series capacitor
Vp_c = I * R  # Peak voltage that needs to be applied from the audio amplifier with a series capacitor added

Vpa = 2 * Vp  # DC power amplifier voltage (Max amount we can handle; max amount voltage capacitor can put out)

Cs = 1 / (L * w**2)  # Series capacitance needed to cancel inductance

P = 0.5 * I**2 * R

# Print results
print(f"Magnetic moment (m): {m:.2f} Am^2")
print(f"Resistance (R): {R:.6f} Ohms")
print(f"Inductance (L): {L:.6f} H")
print(f"Impedance magnitude (|Z|): {magZ:.6f} Ohms")
print(f"Peak voltage without capacitor (Vp): {Vp:.2f} V")
print(f"Peak voltage with capacitor (Vp_c): {Vp_c:.2f} V")
print(f"DC power amplifier voltage (Vpa): {Vpa:.2f} V")
print(f"Series capacitance (Cs): {Cs:.6f} F")
print(f"Power (P): {P:.2f} W")
print(f"Total Wire needed (ft): {perimiter_feet*N:.2f} ft") 
