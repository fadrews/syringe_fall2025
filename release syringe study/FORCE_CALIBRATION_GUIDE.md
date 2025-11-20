# Converting Voltage Ratios to Newtons

## Overview

To convert the voltage ratio readings to force (Newtons), you need to establish a calibration curve by measuring known forces.

## Calibration Process

### 1. **Physical Calibration**

Apply known weights/forces to your sensor and record the voltage ratio readings:

```
Force (N)    Voltage Ratio
0            0.00000000  (zero offset - already calibrated)
0.1          0.00005432
0.2          0.00010865
0.5          0.00027163
1.0          0.00054325
2.0          0.00108650
```

### 2. **Linear Calibration (Simple)**

If the relationship is linear, calculate the slope:

**Formula:** `Force (N) = slope × (Calibrated_Voltage_Ratio)`

**Example:**
- At 1.0 N: Voltage Ratio = 0.00054325
- Slope = 1.0 / 0.00054325 = 1841.0 N per V/V

```python
force_N = 1841.0 * calibrated_voltage_ratio
```

### 3. **Non-Linear Calibration (Polynomial)**

If non-linear, fit a polynomial:

**Formula:** `Force = a₀ + a₁×V + a₂×V² + a₃×V³`

```python
import numpy as np

# Calibration data
voltage_ratios = [0.0, 0.00005432, 0.00010865, 0.00027163, 0.00054325, 0.00108650]
forces = [0.0, 0.1, 0.2, 0.5, 1.0, 2.0]

# Fit polynomial (degree 2 or 3)
coeffs = np.polyfit(voltage_ratios, forces, 2)
# Returns: [a₂, a₁, a₀]

# Convert voltage to force
force_N = np.polyval(coeffs, calibrated_voltage_ratio)
```

## Implementation Options

### Option A: Post-Processing (Recommended)

Convert data after collection using your analysis software (Python, MATLAB, R, Excel):

**Python Example:**
```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('viscosity_data_6_20250124_153045.csv', comment='#')

# Define calibration slope (from your calibration)
SLOPE = 1841.0  # N per V/V (example)

# Convert to Newtons
df['Force_N'] = df['Calibrated_Reading'] * SLOPE

# Save with force data
df.to_csv('viscosity_data_with_force.csv', index=False)
```

**Excel Example:**
```
1. Open CSV in Excel
2. Add column "Force_N"
3. Formula: =G2*1841.0
   (where G is Calibrated_Reading column)
4. Copy formula down
```

### Option B: Real-Time Conversion (In Program)

Add conversion to the program itself.

## Adding Force Conversion to Program

### 1. **Add to Config File**

```json
{
    "force_calibration": {
        "enabled": true,
        "type": "linear",
        "slope": 1841.0,
        "offset": 0.0
    }
}
```

Or for polynomial:
```json
{
    "force_calibration": {
        "enabled": true,
        "type": "polynomial",
        "coefficients": [0.0, 1841.0, 0.0]
    }
}
```

### 2. **Modify Data Collection**

Add force calculation in `collect_data()`:

```python
# Apply calibration offset
offset = self.calibration.get(self.current_channel, 0.0)
calibrated_reading = raw_reading - offset

# Convert to force if enabled
if CONFIG.get('force_calibration', {}).get('enabled', False):
    cal_type = CONFIG['force_calibration']['type']
    if cal_type == 'linear':
        slope = CONFIG['force_calibration']['slope']
        force_N = calibrated_reading * slope
    elif cal_type == 'polynomial':
        coeffs = CONFIG['force_calibration']['coefficients']
        force_N = np.polyval(coeffs, calibrated_reading)
else:
    force_N = None

# Store data
self.data[self.current_channel].append({
    'timestamp': relative_timestamp,
    'trial': self.trial_index,
    'viscosity': self.current_viscosity,
    'channel': self.current_channel,
    'gain': gain,
    'raw': raw_reading,
    'calibrated': calibrated_reading,
    'force_N': force_N  # Add force
})
```

### 3. **Update CSV Output**

```python
writer.writerow(['Trial', 'Viscosity', 'Channel', 'Gain', 'Timestamp', 
                'Raw_Reading', 'Calibrated_Reading', 'Force_N'])

writer.writerow([
    entry['trial'],
    entry['viscosity'],
    entry.get('channel', channel),
    entry.get('gain', CONFIG['bridge_gain']),
    entry['timestamp'],
    entry['raw'],
    entry['calibrated'],
    entry.get('force_N', '')  # Empty if not calculated
])
```

## Determining Your Calibration Factor

### Method 1: Known Weights

1. Hang known masses from sensor
2. Record voltage ratio for each
3. Plot Force vs Voltage Ratio
4. Calculate slope or fit curve

**Example:**
```
Mass (g)  Force (N)   Voltage Ratio    
0         0.000       0.00000000
10        0.098       0.00005324
50        0.490       0.00026621
100       0.981       0.00053242
200       1.962       0.00106484

Slope = 1.962 / 0.00106484 = 1842.5 N per V/V
```

### Method 2: Reference Force Gauge

1. Apply force using calibrated force gauge
2. Record both gauge and voltage ratio
3. Calculate conversion factor

### Method 3: Manufacturer Specs

Check your load cell specifications:
```
Rated Output: 2 mV/V (typical for strain gauge)
Capacity: 10 N
Gain: 128

Sensitivity = (2 mV/V) / (10 N) = 0.2 mV/V per N
With Gain: 0.2 × 128 = 25.6 mV/V per N
Inverse: 1 / 25.6 = 0.0391 N per mV/V = 39.1 N per V/V
```

## Recommendations

### For Your Application:

1. **Do Physical Calibration**
   - Use 3-5 known weights/forces
   - Cover your expected measurement range
   - Repeat 3 times for each weight

2. **Use Post-Processing** (Easier)
   - Collect data in voltage ratios (as currently done)
   - Convert to Newtons in analysis
   - Can adjust calibration later without re-running experiments

3. **Document Everything**
   - Save calibration data
   - Record load cell specs
   - Note gain settings used
   - Keep calibration curve plot

## Example Calibration Script

```python
import numpy as np
import matplotlib.pyplot as plt

# Your calibration data
forces = np.array([0.0, 0.098, 0.490, 0.981, 1.962])  # N
voltage_ratios = np.array([0.0, 0.00005324, 0.00026621, 0.00053242, 0.00106484])  # V/V

# Linear fit
slope, intercept = np.polyfit(voltage_ratios, forces, 1)
print(f"Calibration: Force = {slope:.2f} × VoltageRatio + {intercept:.6f}")

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(voltage_ratios, forces, label='Measured', s=100)
plt.plot(voltage_ratios, slope * voltage_ratios + intercept, 'r-', label='Fit')
plt.xlabel('Voltage Ratio (V/V)')
plt.ylabel('Force (N)')
plt.title('Force Calibration Curve')
plt.legend()
plt.grid(True)
plt.savefig('calibration_curve.png')
plt.show()

print(f"\nSlope: {slope:.2f} N/(V/V)")
print(f"Intercept: {intercept:.6f} N")
print(f"R²: {np.corrcoef(voltage_ratios, forces)[0,1]**2:.6f}")
```

## Quick Conversion Formula

Once you have your slope:

```
Force (N) = Calibration_Slope × Calibrated_Voltage_Ratio
```

Where:
- **Calibration_Slope**: From your calibration (e.g., 1841.0 N per V/V)
- **Calibrated_Voltage_Ratio**: From your data file (already zeroed)

## Next Steps

1. Perform physical calibration with known forces
2. Calculate your calibration slope
3. Choose post-processing or real-time conversion
4. Would you like me to add force conversion to the program code?
