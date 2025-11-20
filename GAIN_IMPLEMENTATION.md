# Gain and Counterbalancing Implementation Summary

## Changes Made

### 1. **Bridge Gain Configuration**

#### Added to Config File (`viscosity_config.json`):
```json
{
    "bridge_gain": 128
}
```

#### Default Value:
- **128x** (maximum gain)
- Can be set to: 1, 2, 4, 8, 16, 32, 64, or 128
- Configured in `viscosity_config.json`

#### Implementation:
- **Config Loading**: Gain value loaded at startup from config
- **Channel Connection**: Gain is set when connecting to each Phidget channel
- **Data Collection**: Actual gain value retrieved from hardware and stored with each data point
- **Simulation Mode**: Uses config gain value

### 2. **Gain Setting on Connection**

When connecting to Phidget channels, the program now:
1. Reads `bridge_gain` from config
2. Maps the numeric value to Phidget's BridgeGain enum
3. Calls `vi.setBridgeGain()` for each channel
4. Prints confirmation of gain setting

Example output:
```
🔌 Connecting to PhidgetBridge channels (0-2)...
   Setting bridge gain to: 128x
✅ Channel 0 attached (gain: 128x)
✅ Channel 1 attached (gain: 128x)
✅ Channel 2 attached (gain: 128x)
```

### 3. **Gain in Data Collection**

Each data point now includes:
- **Actual gain from hardware**: `vi.getBridgeGain()`
- **Fallback to config**: If hardware read fails
- **Simulation**: Uses config value

Data structure:
```python
{
    'timestamp': relative_time,
    'trial': trial_number,
    'viscosity': 'A',
    'channel': 0,
    'gain': 128,  # ← NEW
    'raw': 0.00050,
    'calibrated': 0.00000
}
```

### 4. **CSV Output Format**

#### Metadata Header (NEW):
```csv
# Participant ID:, 6
# Counterbalancing Order:, B, C, A
# Bridge Gain:, 128
# Sampling Frequency (Hz):, 20

```

#### Data Columns:
```csv
Trial, Viscosity, Channel, Gain, Timestamp_128X, Raw_Reading, Calibrated_Reading
1,     B,         1,       128,   0.0,            0.00030,     -0.00000
1,     B,         1,       128,   6.4,            0.00031,     0.00001
```

### 5. **Counterbalancing Order**

#### Already Implemented:
- Uses participant ID to determine order
- Cycles through all 6 permutations of [A, B, C]
- Order is displayed in CSV metadata header

Example for different participants:
- **Participant 1**: Order = A, B, C
- **Participant 2**: Order = A, C, B  
- **Participant 3**: Order = B, A, C
- **Participant 4**: Order = B, C, A
- **Participant 5**: Order = C, A, B
- **Participant 6**: Order = C, B, A
- **Participant 7**: Order = A, B, C (cycles back)

### 6. **Configuration Options**

#### Valid Gain Values:
```
1   = Lowest sensitivity (±1000 mV/V range)
2   = ±500 mV/V
4   = ±250 mV/V
8   = ±125 mV/V
16  = ±62.5 mV/V
32  = ±31.25 mV/V
64  = ±15.625 mV/V
128 = Highest sensitivity (±7.8125 mV/V range)
```

#### Choosing Gain:
- **High gain (64, 128)**: For small signals, precise measurements
- **Medium gain (8, 16, 32)**: General purpose
- **Low gain (1, 2, 4)**: For large signals, avoid saturation

### 7. **Example Output File**

**Filename**: `viscosity_data_6_20250124_153045.csv`

**Content**:
```csv
# Participant ID:, 6
# Counterbalancing Order:, B, C, A
# Bridge Gain:, 128
# Sampling Frequency (Hz):, 20

Trial,Viscosity,Channel,Gain,Timestamp_128X,Raw_Reading,Calibrated_Reading
1,B,1,128,0.0,0.00030406,-0.00003393
1,B,1,128,6.4,0.00031234,-0.00002565
1,B,1,128,12.8,0.00032156,-0.00001643
1,B,1,128,19.2,0.00033078,-0.00000721
...
```

### 8. **Files Modified**

1. **phidget_viscosity_final.py**:
   - Added `bridge_gain` to DEFAULT_CONFIG
   - Updated `connect_channels()` to set gain on each channel
   - Updated `collect_data()` to retrieve and store gain
   - Updated `save_all_data()` to write metadata and gain column
   - Updated `on_close()` auto-save with same format

2. **viscosity_config.json**:
   - Added `"bridge_gain": 128` parameter

3. **CONFIG_README.md**:
   - Added documentation for bridge_gain parameter

### 9. **Benefits**

✅ **Configurable Gain**: Easy to adjust for different sensor sensitivities
✅ **Documented in Data**: Gain value recorded with every measurement
✅ **Metadata Header**: Experiment parameters documented in each file
✅ **Counterbalancing Tracked**: Order clearly shown in output
✅ **Auto-Save Compatible**: Same format for manual and auto-save

### 10. **Testing**

To test gain settings:
1. Edit `viscosity_config.json`
2. Change `"bridge_gain"` to desired value (1, 2, 4, 8, 16, 32, 64, or 128)
3. Run program
4. Check console output confirms gain setting
5. Check CSV output includes correct gain value

### 11. **Troubleshooting**

**If gain setting fails:**
- Console will show: "gain setting failed"
- Program continues with default hardware gain
- Gain from hardware will still be recorded in data

**Invalid gain values:**
- Console shows: "Invalid gain X, using default"
- Uses hardware default
- Update config to valid value
