# Complete Feature Summary - Phidget Viscosity Measurement System

## ✅ All Implemented Features

### 1. **Configuration System**
- JSON-based configuration file (`viscosity_config.json`)
- All major parameters configurable
- Automatic default config creation if missing
- See: `CONFIG_README.md`

### 2. **Bridge Gain Control**
- Default: **128x** (maximum sensitivity)
- Configurable via `bridge_gain` in config file
- Valid values: 1, 2, 4, 8, 16, 32, 64, 128
- Set on all channels at connection time
- Actual gain recorded with each data point
- See: `GAIN_IMPLEMENTATION.md`

### 3. **Counterbalancing**
- Automatic based on participant ID
- Cycles through all 6 permutations of conditions
- Example orders:
  - P1: A, B, C
  - P2: A, C, B
  - P3: B, A, C
  - etc.
- Order recorded in CSV metadata

### 4. **Calibration**
- Duration configurable (default 5s)
- Zero-point offset calculated per channel
- Saved per participant: `phidget_calibration_[ID].csv`
- Can recalibrate anytime
- Can skip and use previous calibration

### 5. **Audio Countdown**
- Duration configurable (default 2s)
- Frequency configurable (default 800 Hz)
- Can be enabled/disabled in config
- Plays before each trial starts
- Visual countdown if audio unavailable

### 6. **Automatic Trial Progression**
- Tracks trials per viscosity
- Automatically switches viscosities when complete
- Manual override available (viscosity selector buttons)
- Shows progress: "A (CH0) - 3/5"
- Completion notification with continue option

### 7. **Data Collection**
- Timestamps reset to 0 at trial start
- Relative timing (excludes pause time)
- Timestamps multiplied by 128 in output
- Pause/Resume functionality
- Sampling rate configurable (default 20 Hz)

### 8. **Data Format**

#### CSV Metadata Header:
```
# Participant ID: 6
# Counterbalancing Order: B, C, A
# Bridge Gain: 128
# Sampling Frequency (Hz): 20
```

#### Data Columns:
```
Trial, Viscosity, Channel, Gain, Timestamp_128X, Raw_Reading, Calibrated_Reading
```

### 9. **Plot Display**
- Real-time data visualization
- Initial scale configurable (default 1e-5)
- Auto-scaling (only expands, never shrinks)
- Scale padding configurable (default 20%)
- Resets for each trial

### 10. **Simulation Mode**
- Automatic if no hardware detected
- Generates realistic random data
- Tests all functionality
- Visual indicator: "[SIMULATION]" in title

### 11. **Auto-Save**
- Saves data automatically on exit
- Prevents data loss
- Same format as manual save
- Confirms save in console

### 12. **User Interface**
- CustomTkinter (modern) or Tkinter (fallback)
- Viscosity selector buttons
- Trial progress display
- Pause/Resume controls
- Save/Recalibrate buttons
- Status messages
- Real-time plot

## 📋 Configuration Parameters

```json
{
    "calibration_duration": 5.0,      // Calibration time (seconds)
    "sampling_frequency": 20,          // Data rate (Hz)
    "countdown_duration": 2.0,         // Audio beep length (seconds)
    "num_channels": 3,                 // Number of channels
    "trials_per_viscosity": 5,         // Trials per condition
    "bridge_gain": 128,                // Phidget gain (1-128)
    "audio": {
        "frequency": 800,              // Beep pitch (Hz)
        "enabled": true                // Audio on/off
    },
    "plot": {
        "initial_scale": 0.00001,      // Starting y-axis
        "scale_padding": 1.2           // Expansion factor
    },
    "viscosity_labels": ["A", "B", "C"] // Condition names
}
```

## 📁 Output Files

### Data File Example:
`viscosity_data_6_20250124_153045.csv`
- Includes metadata header
- Participant ID
- Counterbalancing order
- Configuration parameters
- All trial data with gain

### Calibration File Example:
`phidget_calibration_6.csv`
- Per-participant calibration
- One offset per channel
- Reusable across sessions

## 🎯 Typical Workflow

1. **Start Program** → Enter Participant ID
2. **Calibration** → 5-second zero-point capture
3. **Trial 1 (Viscosity B)** → Audio countdown → Record → Stop
4. **Trial 2 (Viscosity B)** → Repeat...
5. **Trial 5 (Viscosity B)** → Auto-switch to C
6. **Continue** → Through all viscosities
7. **Completion** → Option to continue or save & exit
8. **Auto-Save** → Data saved on exit

## 🔧 Key Technical Details

### Phidget Connection:
```python
vi = VoltageRatioInput()
vi.setChannel(channel_num)
vi.setBridgeGain(BridgeGain.BRIDGE_GAIN_128)
vi.openWaitForAttachment(1000)
```

### Data Point Structure:
```python
{
    'timestamp': 0.05,         # Seconds from trial start
    'trial': 1,
    'viscosity': 'B',
    'channel': 1,
    'gain': 128,               # Actual hardware gain
    'raw': 0.00030406,
    'calibrated': -0.00003393  # raw - offset
}
```

### Timestamp Calculation:
```python
relative_time = time.time() - trial_start_time - pause_duration
output_timestamp = relative_time * 128
```

## 📚 Documentation Files

1. **CONFIG_README.md** - Configuration guide
2. **GAIN_IMPLEMENTATION.md** - Gain feature details
3. **DATA_FORMAT_CHANGES.md** - Data format specification
4. **FEATURES_SUMMARY.md** - This file

## 🎉 Complete Features List

✅ JSON configuration system
✅ Configurable bridge gain (1-128x)
✅ Automatic counterbalancing
✅ Per-participant calibration
✅ Audio countdown (configurable)
✅ Automatic trial progression
✅ Pause/Resume functionality
✅ Real-time plotting with auto-scale
✅ Relative timestamps (0-based per trial)
✅ Timestamp scaling (×128)
✅ Gain recording per data point
✅ Metadata in CSV header
✅ Counterbalancing order in output
✅ Simulation mode
✅ Auto-save on exit
✅ Manual save anytime
✅ Recalibration option
✅ Progress tracking
✅ Modern UI

## 🚀 Ready for Use!

All features implemented and tested. The system is ready for data collection with:
- Proper gain control
- Accurate timestamps
- Complete metadata
- Automatic workflows
- Data safety (auto-save)
