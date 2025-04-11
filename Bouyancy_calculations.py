# Get weights of all parts of the boat
# Get weights from datasheet
# Add conservatism, around 25%
# MARINE BUOYANCY CALCULATOR FOR OFFSHORE RECOVERY VESSEL
# All values in kilograms and liters

# --- CORE COMPONENTS ---
main_structure = 4.76    # PVC pipes (2x30")
em_coil = 2.95           # 80-turn electromagnetic array
servo_system = 0.068     # 68g servo mechanism
drive_motor = 0.500      # 500g propulsion unit
housing = 0.227          # Small PVC component

# --- CONSERVATIVE ADDITIONS ---
connectors_wiring = 0.425  # 5% of main components (screws, wires, etc)

# --- TOTAL WEIGHT ---
total_mass = (
    main_structure 
    + em_coil 
    + servo_system 
    + drive_motor 
    + housing 
    + connectors_wiring
)

# --- BUOYANCY REQUIREMENTS ---
safety_margin = 1.25  # 25% reserve for offshore operations
buoyancy_needed = total_mass * safety_margin

print(f"Total structural weight: {total_mass:.2f} kg")
print(f"Minimum buoyant material volume: {buoyancy_needed:.2f} liters (saltwater)")

# Calculate bouyancy force from PVC, any leftover needs to be accounted for by foam
# alternative to acrylic 

# BUOYANCY DEFICIT CALCULATOR FOR SURFACE BOAT
total_weight = 8.93  # kg (including screws, wires, etc.)
pvc_buoyancy = -1.76  # kg (negative buoyancy from PVC pipes)
safety_factor = 1.25  # 25% safety margin

# Calculate total buoyancy required
required_buoyancy = (total_weight * safety_factor) - pvc_buoyancy
print(f"Required foam buoyancy: {required_buoyancy:.2f} kg\n")

# MATERIAL OPTIONS [kg buoyancy per liter]
materials = {
    "Polyethylene Foam": 0.90,   # Lightweight, cost-effective
    "Polyurethane Foam": 0.85,  # Durable, easy to shape
    "PVC Foam": 0.52            # Structural but less buoyant
}

print("Material        | Volume Needed (liters)")
print("----------------|------------------------")
for material, buoyancy in materials.items():
    volume = required_buoyancy / buoyancy
    print(f"{material:16} | {volume:.1f}")

