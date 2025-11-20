# Data Format Update Summary

## Changes Made to Data Collection and Saving

### 1. **Relative Timestamps (Starting from 0)**
- Each trial now starts with timestamp = 0
- Timestamp is relative to when data collection begins (after countdown)
- Internally stored in seconds from trial start

### 2. **Timestamp Scaling (128X)**
- All timestamps in CSV output are multiplied by 128
- Column header: `Timestamp_128X`
- Formula: `output_timestamp = relative_time * 128`

### 3. **Gain Parameter Added**
- New column in CSV: `Gain`
- Retrieved from Phidget bridge: `vi.getBridgeGain()`
- Default value: 128 (if not available from hardware)
- Simulated gain: 128

### 4. **Updated CSV Format**

#### Old Format:
```
Trial, Viscosity, Channel, Timestamp, Raw_Reading, Calibrated_Reading
```

#### New Format:
```
Trial, Viscosity, Channel, Gain, Timestamp_128X, Raw_Reading, Calibrated_Reading
```

### 5. **Example Data**

#### Trial 1 - Viscosity A:
```
Trial, Viscosity, Channel, Gain, Timestamp_128X, Raw_Reading, Calibrated_Reading
1,     A,         0,       128,   0.0,            0.00050,     0.00000
1,     A,         0,       128,   6.4,            0.00051,     0.00001
1,     A,         0,       128,   12.8,           0.00052,     0.00002
1,     A,         0,       128,   19.2,           0.00053,     0.00003
```

Explanation:
- Sampling at 20 Hz = 0.05s interval
- First sample: time = 0 → 0 * 128 = 0.0
- Second sample: time = 0.05s → 0.05 * 128 = 6.4
- Third sample: time = 0.10s → 0.10 * 128 = 12.8
- Fourth sample: time = 0.15s → 0.15 * 128 = 19.2

#### Trial 2 - Viscosity A (timestamps reset):
```
Trial, Viscosity, Channel, Gain, Timestamp_128X, Raw_Reading, Calibrated_Reading
2,     A,         0,       128,   0.0,            0.00048,     -0.00002
2,     A,         0,       128,   6.4,            0.00049,     -0.00001
...
```

### 6. **Auto-Save on Exit**
- Data automatically saved when closing application (if not already saved)
- Uses same format with gain and timestamp_128x
- Prevents data loss

### 7. **Implementation Details**

#### In `collect_data()`:
```python
# Record trial start time
self.trial_start_time = time.time()  # Set when countdown completes

# During data collection
relative_time = time.time() - self.trial_start_time  # Seconds from start
gain = vi.getBridgeGain()  # Get from hardware

# Store with relative timestamp
entry = {
    'timestamp': relative_time,  # Not multiplied yet
    'gain': gain,
    ...
}
```

#### In `save_all_data()`:
```python
# When saving to CSV
timestamp_128x = entry['timestamp'] * 128  # Multiply by 128
writer.writerow([
    ...,
    entry.get('gain', 128),
    timestamp_128x,
    ...
])
```

### 8. **Benefits**
✅ Each trial starts at timestamp 0 (easier to analyze)
✅ Consistent timestamp scaling factor (128X)
✅ Gain parameter captured for each reading
✅ Backward compatible (can still calculate original time: timestamp_128x / 128)
✅ Auto-save prevents data loss

### 9. **Configuration**
Sampling frequency still controlled by `viscosity_config.json`:
```json
{
    "sampling_frequency": 20
}
```

To change to 100 Hz (0.01s interval):
- Timestamps would be: 0, 1.28, 2.56, 3.84, ... (0.01 * 128 increments)
