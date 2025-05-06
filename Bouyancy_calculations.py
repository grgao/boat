import math

# --- MATERIAL PROPERTIES ---
POLYCARB_DENSITY = 1210      # kg/m³, density of polycarbonate
SALTWATER_DENSITY = 1025     # kg/m³, typical density of seawater

# --- PIPE SPECIFICATIONS ---
NUM_PIPES = 2
OUTER_DIAMETER_IN = 4.5      # Inner diameter in inches
LENGTH_IN = 30               # Length in inches
WEIGHT_PER_FOOT_PVC = 2.01
INCHES_TO_METERS = 0.0254
LB_TO_KG = 0.453592
WIDTH_IN = 24 

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
outer_radius = (OUTER_DIAMETER_IN)*INCHES_TO_METERS / 2
length_m = (LENGTH_IN)*INCHES_TO_METERS
single_pipe_volume = math.pi * (outer_radius ** 2) * length_m
total_pipe_volume = single_pipe_volume * NUM_PIPES # m³

pipe_mass = (WEIGHT_PER_FOOT_PVC * LENGTH_IN / 12)*LB_TO_KG # Weight in KG

# --- TOTAL WEIGHT CALCULATION ---
component_sum = sum(components.values())
contingency = component_sum * 0.05  # 5% contingency
total_weight = component_sum + pipe_mass + contingency

# --- BUOYANCY ANALYSIS ---
displaced_volume = total_pipe_volume
buoyant_force = displaced_volume * SALTWATER_DENSITY  # Buoyant force in kg
safety_margin = 1.25  # 25% safety factor
required_buoyancy = total_weight * safety_margin
required_foam = required_buoyancy - buoyant_force


# --- FOAM BOUYANCY (kg/m³) ---
EPS_FOAM_DENSITY = 22.5  # kg/m³, density of EPS foam
EPS_FOAM_THICKNESS = 2
foam_volume = (length_m * WIDTH_IN * INCHES_TO_METERS) * (EPS_FOAM_THICKNESS * INCHES_TO_METERS)  # m³
foam_bouyancy = SALTWATER_DENSITY * foam_volume  # kg/m³


# --- FOAM MATERIAL OPTIONS (INCLUDING PINK EPS FOAM) ---
# Buoyancy is equal to F= Rho * V * g;
# Weight of item m = density*v
# effective bouyant force Fb = F - g*m


print("[BUOYANCY ANALYSIS]")
print(f"PVC Pipe Mass: {pipe_mass:.2f} kg")
print(f"Total Vessel Weight: {total_weight:.2f} kg")
print(f"Pipe Buoyancy Contribution: {buoyant_force:.2f} kg")
print(f"Total Buoyancy Required: {required_buoyancy:.2f} kg")
print(f"Required Foam Buoyancy: {required_foam:.2f} kg\n")
print(f"Foam Volume: {foam_volume:.4f} m³")
print(f"Foam Bouyancy: {foam_bouyancy:.2f} kg")