import numpy as np
try:
    import magpylib as magpy
except ImportError:
    print("Note: Install magpylib for more accurate B-field calculations: pip install magpylib")

# --------------------------
# Original Loop Design Code
# --------------------------
def rectangle_loop_inductance(W, H, d, N, mu_r=1):
    """Calculate inductance of rectangular loop"""
    mu_0 = 4 * np.pi * 1e-7
    L = (mu_0 * mu_r / np.pi) * (
        -2 * (W + H) + 
        2 * np.sqrt(H**2 + W**2) - 
        H * np.log((H + np.sqrt(H**2 + W**2)) / W) - 
        W * np.log((W + np.sqrt(H**2 + W**2)) / H) + 
        H * np.log(2 * H / (d/2)) + 
        W * np.log(2 * W / (d/2))
    )
    return L * N**2

# Loop parameters
N = 50                # Number of turns
I_peak = 1            # Peak current (A)
W, H = 0.91, 0.61     # Loop dimensions (m)
d_wire = 0.001        # Wire diameter (m)
f = 30                # Frequency (Hz)
rl = 20.9 / 1000      # Resistance per meter (#18 AWG)

# Calculate electrical properties
A = W * H
perimeter = 2 * (W + H)
R = perimeter * N * rl
L = rectangle_loop_inductance(W, H, d_wire, N)
w = 2 * np.pi * f
Zl = w * L
magZ = np.sqrt(R**2 + Zl**2)
m = N * I_peak * A     # Magnetic moment

# --------------------------
# Magnetic Field Calculations
# --------------------------
def calculate_B_field(loop_params, obs_point):
    """Calculate B-field using multiple methods"""
    W, H, N, I = loop_params
    results = {}
    
    # Method 1: Magpylib (most accurate)
    if 'magpy' in globals():
        loop = magpy.current.Loop(
            current=N*I,
            diameter=np.sqrt(W**2 + H**2),
            position=(W/2, H/2, 0)
        )
        results['Magpylib'] = loop.getB(obs_point)
    
    # Method 2: Biot-Savart Approximation
    num_segments = 100  # Per side
    dl = W/num_segments
    B_bs = np.zeros(3)
    
    # Segment discretization
    for side in ['bottom', 'right', 'top', 'left']:
        for i in range(num_segments):
            if side == 'bottom':
                x = i*dl
                segment = np.array([x, 0, 0])
                dvec = np.array([dl, 0, 0])
            elif side == 'right':
                y = i*dl
                segment = np.array([W, y, 0])
                dvec = np.array([0, dl, 0])
            elif side == 'top':
                x = W - i*dl
                segment = np.array([x, H, 0])
                dvec = np.array([-dl, 0, 0])
            else:  # left
                y = H - i*dl
                segment = np.array([0, y, 0])
                dvec = np.array([0, -dl, 0])
            
            r = obs_point - (segment + dvec/2)
            r_mag = np.linalg.norm(r)
            B_bs += np.cross(dvec, r) / r_mag**3
    
    B_bs *= (4*np.pi*1e-7) * N*I / (4*np.pi)
    results['Biot-Savart'] = B_bs
    
    return results

# --------------------------
# Analysis and Output
# --------------------------
if __name__ == "__main__":
    # Observation point (1 meter above center)
    obs_point = np.array([W/2, H/2, 1])
    
    # Calculate magnetic field
    B_fields = calculate_B_field((W, H, N, I_peak), obs_point)
    
    # Print electrical parameters
    print("=== Loop Electrical Parameters ===")
    print(f"Magnetic Moment (m): {m:.2f} Am² (Target: 50-100 Am²)")
    print(f"Resistance: {R:.2f} Ω")
    print(f"Inductance: {L:.4f} H")
    print(f"Impedance @ {f} Hz: {magZ:.2f} Ω")
    print(f"Required Voltage: {I_peak*magZ:.2f} V\n")
    
    # Print magnetic field results
    print("=== Magnetic Field Calculations ===")
    print(f"At observation point {obs_point} meters:")
    for method, B in B_fields.items():
        print(f"{method}:")
        print(f"  B = [{B[0]:.2e}, {B[1]:.2e}, {B[2]:.2e}] T")
        print(f"  |B| = {np.linalg.norm(B):.2e} T")
        print(f"  ({np.linalg.norm(B)*1e6:.2f} µT)")
    
    # Optimization suggestions
    print("\n=== Optimization Suggestions ===")
    if m < 50:
        req_factor = 50/m
        print(f"Increase parameters by {req_factor:.1f}x to reach 50 Am²:")
        print(f"- Current to {I_peak*req_factor:.1f} A")
        print(f"- Turns to {N*req_factor:.0f}")
        print(f"- Area to {A*req_factor:.2f} m² (e.g., {np.sqrt(A*req_factor)*1.2:.2f}m x {np.sqrt(A*req_factor)*0.8:.2f}m)")