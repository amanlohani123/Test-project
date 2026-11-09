# M.Tech Project - 3 Phase Induction Motor Basic Calculation
import math

# Motor ki basic ratings
V_line = 415      # Line voltage in volts
frequency = 50    # Supply frequency in Hz
poles = 4         # Number of poles

# Phase voltage nikal rahe hain
V_phase = V_line / 1.732

# Synchronous speed (RPM me)
Ns = (120 * frequency) / poles
print("Synchronous Speed (RPM):", Ns)

# Equivalent circuit ke parameters (assume kiye hain)
R1 = 0.5     # Stator resistance
X1 = 1.0     # Stator reactance
R2 = 0.4     # Rotor resistance
X2 = 1.0     # Rotor reactance
Xm = 35.0    # Magnetization reactance

# Alag alag slip par performance check kar rahe hain
slip_values = [1.0, 0.08, 0.05, 0.02]

print("\n--- Slip wise motor calculation ---")
for s in slip_values:
    # Rotor ka slip resistance term
    r2_slip = R2 / s
    
    # Total impedance aur current ka hisaab
    # Parallel branch ka equivalent
    denom_real = r2_slip
    denom_imag = X2 + Xm
    mag_denom = math.sqrt(denom_real**2 + denom_imag**2)
    
    # Approximate stator current 
    I_stator = V_phase / math.sqrt((R1 + r2_slip)**2 + (X1 + X2)**2)
    
    # Torque ka formula
    ws = (2 * math.pi * Ns) / 60
    P_ag = 3 * (I_stator ** 2) * r2_slip
    torque = P_ag / ws
    
    # Speed rotor ki
    Nr = Ns * (1 - s)
    
    print(f"Slip: {s} | Speed: {Nr:.1f} RPM | Current: {I_stator:.2f} A | Torque: {torque:.2f} Nm")

print("\nSimulation completed successfully without errors.")
