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

# Constants
METER_TO_FEET = 3.28084
FEET_TO_METER = 1 / METER_TO_FEET
LB_TO_KG = 0.453592
RL_18AWG = 20.9 / 1000  # Ohms per m of wire for #18 AWG
RL_20AWG = 33.2 / 1000 # Ohms per m of wire for #20 AWG
WEIGHT_18AWG = 0.010 # lbs/ft
WEIGHT_20AWG = 0.0048 # lbs/ft

wires = {
    "18AWG": {
        "resistance": RL_18AWG,
        "weight": WEIGHT_18AWG,
        "diameter": 1.02e-3 # mm
    },
    "20AWG": {
        "resistance": RL_20AWG,
        "weight": WEIGHT_20AWG,
        "diameter": 0.8128e-3 # mm
    }
}

# We want to minimize power and weight, so minimize current 1st, then number of turns
N = 78 # Coil has been wound with 78 turns, need to solder for more. 
I = 1.63  # Peak AC current, divide by sqrt2 for RMS current

width = 2 * FEET_TO_METER # 2 ft loop
height = 30/12 * FEET_TO_METER # 2.5 ft loop

A = width * height 
f = 30  # frequency that you are driving the loop at. This small signal comes from the Raspberry Pi.
w = 2 * np.pi * f

magnetic_moment = N * I * A  # N is the number of turns, I is the current in the wire, and A is the area of the loop.

perimiter = height * 2 + width * 2

# Select wire type
for wire_type in wires:
    print(f"Wire type: {wire_type}")
    wire = wires[wire_type]

    R = perimiter * N * wire["resistance"]  # Resistance of coil
    perimiter_feet = perimiter * METER_TO_FEET
    weight_wire = perimiter_feet * wire["weight"] * N  # Weight of wire in lbs

    # Inductance?
    # https://www.allaboutcircuits.com/tools/rectangle-loop-inductance-calculator/

    # TODO: Update so that inductance isn't hard coded
    L = rectangle_loop_inductance(width, height, wire['diameter'], N)

    Zl = w * L
    magZ = np.sqrt(R**2 + Zl**2)

    Vp = I * magZ  # Peak voltage that needs to be applied to the loop from the audio amplifier without series capacitor
    Vp_c = I * R  # Peak voltage that needs to be applied from the audio amplifier with a series capacitor added

    Vpa = 2 * Vp  # DC power amplifier voltage (Max amount we can handle; max amount voltage capacitor can put out)

    Cs = 1 / (L * w**2)  # Series capacitance needed to cancel inductance

    average_loop_power = 0.5 * I**2 * R

    # Print results
    print(f"Magnetic moment (m): {magnetic_moment:.2f} Am^2")
    print(f"Area (A): {A:.6f} m^2")

    print(f"Resistance (R): {R:.6f} Ohms")
    print(f"Inductance (L): {L:.6f} H")
    print(f"Impedance magnitude (|Z|): {magZ:.6f} Ohms")
    print(f"Peak voltage without capacitor (Vp): {Vp:.2f} V")
    print(f"Peak voltage with capacitor (Vp_c): {Vp_c:.2f} V")
    print(f"DC power amplifier voltage (Vpa): {Vpa:.2f} V")
    print(f"Series capacitance (Cs): {Cs*10**3:.6f} mF")
    print(f"Power (P): {average_loop_power:.2f} W")
    print(f"Total Wire needed (ft): {perimiter_feet*N:.2f} ft") 
    print(f"Total Weight of Wire (kg): {weight_wire:.2f} lb")
    print()