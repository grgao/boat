import numpy as np

# Goal: design a transmitting loop, with a mag. moment = 50-100 Am^2

def rectangle_loop_inductance(W, H, d, N, mu_r=1):
    """
    Calculate the inductance of a rectangular loop.
    
    Args:
    W (float): Width of the loop in meters
    H (float): Height of the loop in meters
    d (float): Diameter of the wire in meters
    N (int): Number of turns in the loop
    mu_r (float): Relative permeability of the medium (default is 1 for air)
    
    Returns:
    float: Inductance in henries (H)
    """
    mu_0 = 4 * np.pi * 1e-7  # permeability of free space
    
    L = (mu_0 * mu_r / np.pi) * (
        -2 * (W + H) + 
        2 * np.sqrt(H**2 + W**2) - 
        H * np.log((H + np.sqrt(H**2 + W**2)) / W) - 
        W * np.log((W + np.sqrt(H**2 + W**2)) / H) + 
        H * np.log(2 * H / (d/2)) + 
        W * np.log(2 * W / (d/2))
    )
    
    return L * N**2  # Multiply by N^2 for N turns

N = 50 # Number of turns in the loop
I = 1  # Peak AC current
W = 0.91  # Width of the loop in meters
H = 0.61  # Height of the loop in meters
A = W * H  # 2x3 ft loop area
f = 30  # frequency that you are driving the loop at. This small signal comes from the Raspberry Pi.
w = 2 * np.pi * f

m = N * I * A  # N is the number of turns, I is the current in the wire, and A is the area of the loop.

METER_TO_FEET = 3.28084

rl = 20.9 / 1000  # Ohms per meter of wire for #18 AWG

perimeter = 2 * (W + H)
R = perimeter * N * rl

perimeter_feet = perimeter * METER_TO_FEET

# Calculate inductance using the rectangle_loop_inductance function
d = 0.001  # Approximate diameter of #18 AWG wire in meters
L = rectangle_loop_inductance(W, H, d, N)

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
print(f"Total Wire needed (ft): {perimeter_feet*N:.2f} ft")