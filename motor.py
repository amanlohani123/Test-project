# Mtech project - Squirrel Cage Induction Motor Harmonics & Voltage Analysis
import math

print("=== Squirrel Cage Induction Motor Performance & Harmonic Analysis ===")

# User se values le rahe hai
v_in = input("Enter Line Voltage in Volts (default 415): ")
V_line = 415 if v_in.strip() == "" else float(v_in)

f_in = input("Enter Frequency in Hz (default 50): ")
frequency = 50 if f_in.strip() == "" else float(f_in)

# Harmonics kon sa dalna hai (jaise 5th ya 7th)
h_in = input("Enter Harmonic Order to check (e.g., 5 or 7, enter 0 for clean supply): ")
harmonic_order = 0 if h_in.strip() == "" else int(h_in)

thd_in = input("Enter Harmonic Distortion percentage (e.g., 10 for 10%, default 0): ")
thd_pct = 0.0 if thd_in.strip() == "" else float(thd_in)

# Motor ke basic poles
poles = 4
V_phase = V_line / 1.732

# Agar harmonics hai toh voltage aur reactance par asar padega
print(f"\nRunning analysis for Voltage: {V_line}V, Frequency: {frequency}Hz")
if harmonic_order > 0 and thd_pct > 0:
    print(f"-> Applying {harmonic_order}th Harmonic with {thd_pct}% distortion...")
    # Harmonics ki wajah se effective voltage thoda badh jata hai losses ke sath
    effective_voltage = V_phase * (1 + (thd_pct / 100))
else:
    print("-> Running with clean sinusoidal supply...")
    effective_voltage = V_phase

# Sync speed nikal rhe hai
Ns = (120 * frequency) / poles
print("Synchronous Speed (RPM):", Ns)

# Motor equivalent circuit parameters (Squirrel Cage Motor)
R1 = 0.45
X1 = 0.8
R2 = 0.35
X2 = 0.82

# Alag alag slip par check kar rhe hai
slips = [1.0, 0.1, 0.05, 0.02]

print("\n--- Performance Results & Feasibility Check ---")
for s in slips:
    r2_s = R2 / s
    
    # Harmonic frequency ke hisab se reactance change hoga
    freq_factor = harmonic_order if harmonic_order > 0 else 1.0
    x_total = X1 + (X2 * freq_factor * (1 + thd_pct/100 if thd_pct > 0 else 1.0))
    
    # Stator current calculation
    I = effective_voltage / math.sqrt((R1 + r2_s)**2 + x_total**2)
    
    # Torque nikalo (5th harmonic backward torque deta hai, 7th forward)
    ws = (2 * math.pi * Ns) / 60
    pag = 3 * (I ** 2) * r2_s
    tq = pag / ws
    
    if harmonic_order == 5:
        tq = tq * 0.82  # 5th harmonic reduces torque due to counter rotation
    elif harmonic_order == 7:
        tq = tq * 1.04  # 7th harmonic adds slight pulsating torque
        
    # Rotor speed
    nr = Ns * (1 - s)
    
    # Feasibility aur unfeasible check karne ki logic
    if I > 70.0:
        st = "Unfeasible (High Current / Overheating Risk due to Harmonics)"
    elif thd_pct > 12.0:
        st = "Feasible with High Harmonic Losses (Warning)"
    else:
        st = "Normal / Feasible Operation"
        
    print(f"Slip: {s} | Speed: {nr:.1f} RPM | Current: {round(I, 2)} A | Torque: {round(tq, 2)} Nm | Status: {st}")

print("\nSimulation completed successfully without errors!")
