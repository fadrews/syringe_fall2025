# Viscosity Measurement System - Configuration Guide

## Configuration File: `viscosity_config.json`

This file controls all major settings for the viscosity measurement system.

### Configuration Options

#### **calibration_duration** (number, seconds)
- Default: `5.0`
- How long to collect baseline data during calibration
- Longer duration = more accurate baseline

#### **sampling_frequency** (number, Hz)
- Default: `20`
- How many samples per second to collect
- Higher = more data points but larger files
- Common values: 10, 20, 50, 100

#### **countdown_duration** (number, seconds)
- Default: `2.0`
- Length of audio beep before recording starts
- Gives participant time to prepare

#### **num_channels** (number)
- Default: `3`
- How many Phidget channels to connect (0, 1, 2, ...)
- Must match your viscosity_labels array length

#### **trials_per_viscosity** (number)
- Default: `5`
- Default number of trials to run per viscosity
- Can be changed in GUI, this is just the starting value

#### **bridge_gain** (number)
- Default: `128`
- Phidget bridge amplifier gain setting
- Valid values: 1, 2, 4, 8, 16, 32, 64, 128
- Higher gain = more sensitive measurements
- Set based on expected signal strength
- Applied to all channels when connecting

#### **audio** (object)
- **frequency** (number, Hz)
  - Default: `800`
  - Pitch of the countdown beep
  - Range: 37-32767 Hz (higher = higher pitch)
  
- **enabled** (boolean)
  - Default: `true`
  - Set to `false` to disable audio countdown
  - Timing still works, just no sound

#### **plot** (object)
- **initial_scale** (number)
  - Default: `0.00001` (1e-5)
  - Starting y-axis range (0 to this value)
  - Automatically expands if data exceeds this
  - Use scientific notation: 0.00001 or 1e-5
  
- **scale_padding** (number)
  - Default: `1.2`
  - How much to expand scale when data exceeds current range
  - 1.2 = 20% padding above max value
  - 1.5 = 50% padding

#### **viscosity_labels** (array of strings)
- Default: `["A", "B", "C"]`
- Labels for each channel/viscosity
- Length must match num_channels
- Can use any labels: ["Low", "Medium", "High"], ["V1", "V2", "V3"], etc.

### Example Configurations

#### High-Speed Sampling
```json
{
    "sampling_frequency": 100,
    "calibration_duration": 10.0,
    ...
}
```

#### 4 Channels with Custom Labels
```json
{
    "num_channels": 4,
    "viscosity_labels": ["Water", "Glycerin", "Oil", "Honey"],
    ...
}
```

#### Silent Mode (No Audio)
```json
{
    "audio": {
        "enabled": false
    },
    ...
}
```

#### High-Resolution Plot
```json
{
    "plot": {
        "initial_scale": 0.000001,
        "scale_padding": 1.1
    },
    ...
}
```

### Notes

- JSON format requires:
  - Double quotes around property names and strings
  - No trailing commas
  - `true`/`false` (lowercase, no quotes)
  - Numbers without quotes
  
- If config file is missing or invalid, system uses default values
- System automatically creates default config on first run
- Edit the file and restart the program to apply changes

### Troubleshooting

**Error: "Expecting property name enclosed in double quotes"**
- Make sure all property names have double quotes
- Remove any comments (// or /* */)
- Check for trailing commas

**Config not loading**
- Verify file is named exactly `viscosity_config.json`
- Check file is in same directory as the Python script
- Validate JSON syntax at jsonlint.com

**Values not taking effect**
- Restart the program after editing config
- Check console output to confirm values loaded
- Verify JSON syntax is correct
