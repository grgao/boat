import numpy as np

def square_loop_analysis(side_length=2.5, target_moment=(50, 100)):
    """
    Comprehensive analysis of square loop electromagnetic properties
    Returns feasible configurations meeting target magnetic moment requirements
    """
    # Constants
    mu_0 = 4 * np.pi * 1e-7  # Permeability of free space (T·m/A)
    perimeter = 4 * side_length
    area = side_length ** 2
    
    # Wire gauge database (AWG: [diameter_mm, resistance_ohm/m, max_current_A])
    wire_gauges = {
        10: {'diam_mm': 2.59, 'res_per_m': 0.00328, 'max_current': 30},
        14: {'diam_mm': 1.63, 'res_per_m': 0.00829, 'max_current': 15},
        18: {'diam_mm': 1.02, 'res_per_m': 0.0210, 'max_current': 7},
        22: {'diam_mm': 0.644, 'res_per_m': 0.0530, 'max_current': 3},
        30: {'diam_mm': 0.255, 'res_per_m': 0.339, 'max_current': 0.5}
    }

    results = []
    
    for awg, specs in wire_gauges.items():
        # Calculate maximum possible turns
        max_turns = int(perimeter / (specs['diam_mm'] * 1e-3))  # Convert mm to m
        
        for turns in [10, 100, max_turns//2, max_turns]:  # Test practical turn counts
            if turns < 1:
                continue
                
            # Current requirements calculation
            I_min = target_moment[0] / (area * turns)
            I_max = target_moment[1] / (area * turns)
            
            # Skip if current exceeds wire capacity
            if I_max > specs['max_current']:
                continue
                
            # Resistance calculation
            wire_length = perimeter * turns
            resistance = wire_length * specs['res_per_m']
            
            # Inductance calculation (simplified loop formula)
            inductance = mu_0 * (turns**2) * side_length / 2
            
            # Voltage requirement
            voltage_min = I_min * resistance
            voltage_max = I_max * resistance
            
            results.append({
                'AWG': awg,
                'Turns': turns,
                'Current_Range_A': (round(I_min, 2), round(I_max, 2)),
                'Resistance_Ω': round(resistance, 3),
                'Inductance_H': round(inductance, 5),
                'Voltage_Range_V': (round(voltage_min, 2), round(voltage_max, 2)),
                'Feasible': I_max <= specs['max_current']
            })
    
    return results

# Run analysis with default parameters
analysis_results = square_loop_analysis()

# Print formatted results
print(f"{'AWG':<5}{'Turns':<7}{'Current (A)':<15}{'Resistance':<12}{'Inductance':<12}{'Voltage (V)':<15}Feasible")
for result in analysis_results:
    if result['Feasible']:
        print(f"{result['AWG']:<5}{result['Turns']:<7}"
              f"{result['Current_Range_A'][0]}-{result['Current_Range_A'][1]:<15}"
              f"{result['Resistance_Ω']:<12}"
              f"{result['Inductance_H']:<12}"
              f"{result['Voltage_Range_V'][0]}-{result['Voltage_Range_V'][1]:<15}"
              f"{'✅' if result['Feasible'] else '❌'}")
