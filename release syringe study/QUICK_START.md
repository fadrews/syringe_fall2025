# Quick Start Guide

## Files You Need

1. **phidget_viscosity_final.py** - Main program (USE THIS ONE!)
2. **viscosity_config.json** - Configuration file
3. **CONFIG_README.md** - Configuration documentation
4. **GAIN_IMPLEMENTATION.md** - Gain feature details

## First Time Setup

### 1. Install Requirements
```bash
pip install Phidget22
pip install customtkinter
pip install matplotlib
```

### 2. Configure (Optional)
Edit `viscosity_config.json` to change:
- Bridge gain (default: 128)
- Number of trials per viscosity (default: 5)
- Sampling frequency (default: 20 Hz)
- Audio settings
- Etc.

## Running the Program

### Start
```bash
python phidget_viscosity_final.py
```

### Workflow
1. Enter participant ID
2. Connect to Phidget (or run in simulation)
3. Calibrate sensors (5 seconds)
4. Run trials:
   - Select viscosity (or use automatic progression)
   - Press "Start Trial"
   - Audio countdown (2 seconds)
   - Data collection begins
   - Press "Stop Trial" when done
5. Repeat until all trials complete
6. Save data (or auto-saves on exit)

## Key Features

### Bridge Gain
- **Default: 128x** (highest sensitivity)
- Change in `viscosity_config.json`
- Valid: 1, 2, 4, 8, 16, 32, 64, 128

### Counterbalancing
- **Automatic** based on participant ID
- Order shown in CSV metadata

### Data Output
- **Format**: CSV with metadata header
- **Columns**: Trial, Viscosity, Channel, Gain, Timestamp_128X, Raw, Calibrated
- **Auto-save**: On exit (if not manually saved)

## Configuration Examples

### High-Speed Sampling (100 Hz)
```json
{
    "sampling_frequency": 100,
    ...
}
```

### Lower Gain for Large Signals
```json
{
    "bridge_gain": 8,
    ...
}
```

### 10 Trials Per Viscosity
```json
{
    "trials_per_viscosity": 10,
    ...
}
```

### Disable Audio
```json
{
    "audio": {
        "enabled": false
    },
    ...
}
```

## Troubleshooting

### No Phidgets Detected
- Check USB connection
- Install Phidget22 drivers
- Or run in simulation mode

### Audio Not Working
- Check system volume
- Or disable in config

### Data Not Saving
- Check write permissions
- Data auto-saves on exit

## Output Files

### Data File
`viscosity_data_[ParticipantID]_[Timestamp].csv`

Example: `viscosity_data_6_20250124_153045.csv`

### Calibration File
`phidget_calibration_[ParticipantID].csv`

Example: `phidget_calibration_6.csv`

## Support

See documentation:
- **CONFIG_README.md** - Full configuration guide
- **GAIN_IMPLEMENTATION.md** - Gain details
- **DATA_FORMAT_CHANGES.md** - Data format spec
- **FEATURES_SUMMARY.md** - All features

## Quick Tips

✅ Config file is created automatically with defaults if missing
✅ Calibration is saved per participant (reusable)
✅ Data auto-saves on exit (don't lose data!)
✅ Can pause/resume trials
✅ Can recalibrate anytime
✅ Timestamps start at 0 for each trial
✅ Gain is recorded with every data point
✅ Counterbalancing order in CSV metadata
