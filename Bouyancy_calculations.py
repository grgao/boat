import math

# --- MATERIAL PROPERTIES ---
POLYCARB_DENSITY = 1210      # kg/m³, density of polycarbonate
SALTWATER_DENSITY = 1025     # kg/m³, typical density of seawater

# --- PIPE SPECIFICATIONS ---
NUM_PIPES = 2
INNER_DIAMETER_IN = 4.0      # Inner diameter in inches
LENGTH_IN = 30               # Length in inches

def in_to_m(inches):
    """Convert inches to meters."""
    return inches * 0.0254

# --- COMPONENT WEIGHTS (UPDATED WITH SOLAR PANEL) ---
components = {
    'em_coil': 2.95,         # Electromagnetic coil
    'servo': 0.068,          # Servo motor
    'motor': 0.500,          # Propulsion motor
    'battery': 1.80,         # LiFePO4 battery
    'small_pvc': 0.227,      # PVC housing
    'solar_panel': 6.00      # 6kg solar panel
}

# --- CALCULATE PIPE MASS USING INNER DIAMETER ---
inner_radius = in_to_m(INNER_DIAMETER_IN) / 2
length_m = in_to_m(LENGTH_IN)
single_pipe_volume = math.pi * (inner_radius ** 2) * length_m
total_pipe_volume = single_pipe_volume * NUM_PIPES
pipe_mass = total_pipe_volume * POLYCARB_DENSITY

# --- TOTAL WEIGHT CALCULATION ---
component_sum = sum(components.values())
contingency = component_sum * 0.05  # 5% contingency
total_weight = component_sum + pipe_mass + contingency

# --- BUOYANCY ANALYSIS ---
displaced_volume = total_pipe_volume
buoyant_force = displaced_volume * SALTWATER_DENSITY
safety_margin = 1.25  # 25% safety factor
required_buoyancy = total_weight * safety_margin
required_foam = required_buoyancy - buoyant_force

# --- FOAM MATERIAL OPTIONS (INCLUDING PINK EPS FOAM) ---
foams = {
    'Polyethylene': 0.90,    # Marine foam
    'Polyurethane': 0.85,    # Marine foam
    'PVC Foam': 0.52,        # Structural
    'Syntactic Foam': 0.88,  # Deep water
    'Pink EPS Foam': 0.98    # 2 lb/ft³ density (~32 kg/m³)
}

print("[BUOYANCY ANALYSIS]")
print(f"Polycarbonate Pipe Mass: {pipe_mass:.2f} kg")
print(f"Total Vessel Weight: {total_weight:.2f} kg")
print(f"Pipe Buoyancy Contribution: {buoyant_force:.2f} kg")
print(f"Total Buoyancy Required: {required_buoyancy:.2f} kg")
print(f"Required Foam Buoyancy: {required_foam:.2f} kg\n")

print("[FOAM VOLUME REQUIREMENTS]")
print("Material         | Volume Needed (liters) | Example Thickness (cm)")
print("-----------------|------------------------|-----------------------")

for material, buoyancy in foams.items():
    volume = required_foam / buoyancy if required_foam > 0 else 0
    thickness = (volume * 1000) / (30 * 15)  # 30x15cm base area
    print(f"{material:16} | {volume:8.1f}              | {thickness:5.1f}")
