# Phidget Viscosity Measurement System
## Complete Software Documentation

---

## Table of Contents

1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Configuration](#configuration)
6. [User Interface](#user-interface)
7. [Workflow](#workflow)
8. [Data Output](#data-output)
9. [Features](#features)
10. [Troubleshooting](#troubleshooting)
11. [Technical Details](#technical-details)
12. [File Reference](#file-reference)

---

## Overview

### Purpose
The Phidget Viscosity Measurement System is a data acquisition application for measuring force/viscosity using Phidget bridge sensors. It's designed for experimental research with multiple conditions (viscosities) and automatic counterbalancing.

### Version
- **Software**: V3.1
- **Last Updated**: October 2024

### Key Capabilities
- Multi-channel force sensing (up to 3 channels)
- Automatic counterbalancing of conditions
- Real-time data visualization
- Configurable bridge gain (1-128x)
- Pause/resume during trials
- Automatic trial progression
- CSV data export with metadata

---

## System Requirements

### Hardware
- **Phidget Bridge Device** (e.g., PhidgetBridge 4-Input)
- **Load cells/strain gauges** connected to bridge channels
- **Computer**: Windows, macOS, or Linux
- **USB port** for Phidget connection

### Software
- **Python**: 3.7 or higher
- **Required Libraries**:
  - `Phidget22` - Phidget device control
  - `customtkinter` - Modern UI (optional, falls back to tkinter)
  - `matplotlib` - Data plotting
  - `numpy` - Numerical operations (optional)

### Operating Systems
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 20.04+)

---

## Installation

### Step 1: Install Python
Download and install Python 3.7+ from [python.org](https://www.python.org/downloads/)

### Step 2: Install Phidget Drivers
1. Download Phidget22 drivers from [phidgets.com](https://www.phidgets.com/downloads/)
2. Install the drivers for your operating system
3. Restart computer if prompted

### Step 3: Install Python Libraries

```bash
# Required
pip install Phidget22
pip install matplotlib

# Recommended (for modern UI)
pip install customtkinter

# Optional (for advanced analysis)
pip install numpy
pip install pandas
```

### Step 4: Download Software Files
Place these files in the same directory:
- `phidget_viscosity_final.py` - Main program
- `viscosity_config.json` - Configuration file
- Documentation files (optional)

### Step 5: Connect Hardware
1. Connect load cells to Phidget Bridge channels
2. Connect Phidget Bridge to computer via USB
3. Verify connection (device LED should light up)

---

## Quick Start

### Running the Program

```bash
cd /path/to/program
python phidget_viscosity_final.py
```

### First Run Workflow

1. **Enter Participant ID**
   - Dialog appears on startup
   - Enter numeric or alphanumeric ID
   - Used for counterbalancing and file naming

2. **Hardware Detection**
   - Program searches for Phidget devices
   - If not found, offers simulation mode
   - Simulation mode generates random data for testing

3. **Calibration**
   - 5-second zero-point calibration
   - Don't touch sensors during calibration
   - Can skip if using previous calibration

4. **Main Interface Opens**
   - Ready to start trials
   - All controls visible

5. **Run First Trial**
   - Click "Start Trial"
   - 2-second audio countdown
   - Recording begins automatically
   - Click "Stop Trial" when done

6. **Save Data**
   - Click "Save Data" anytime
   - Or data auto-saves on exit

---

## Configuration

### Configuration File: `viscosity_config.json`

```json
{
    "calibration_duration": 5.0,
    "sampling_frequency": 20,
    "countdown_duration": 2.0,
    "num_channels": 3,
    "trials_per_viscosity": 5,
    "bridge_gain": 128,
    "audio": {
        "frequency": 800,
        "enabled": true
    },
    "plot": {
        "initial_scale": 0.0001,
        "scale_padding": 1.2
    },
    "viscosity_labels": ["A", "B", "C"]
}
```

### Configuration Parameters

#### **calibration_duration** (seconds)
- Default: `5.0`
- Duration of zero-point calibration
- Longer = more stable baseline
- Range: 1-30 seconds

#### **sampling_frequency** (Hz)
- Default: `20`
- Data samples per second
- Higher = more data points
- Typical: 10-100 Hz
- Note: Very high rates may impact performance

#### **countdown_duration** (seconds)
- Default: `2.0`
- Audio beep duration before trial starts
- Gives user time to prepare
- Range: 0-10 seconds

#### **num_channels** (integer)
- Default: `3`
- Number of Phidget bridge channels to use
- Range: 1-4 (depends on hardware)

#### **trials_per_viscosity** (integer)
- Default: `5`
- Number of trials per condition
- Auto-advances when complete
- Range: 1-100

#### **bridge_gain** (integer)
- Default: `128`
- Phidget bridge amplifier gain
- Valid values: `1, 2, 4, 8, 16, 32, 64, 128`
- Higher = more sensitive
- 128 = maximum sensitivity

#### **audio.frequency** (Hz)
- Default: `800`
- Countdown beep pitch
- Range: 200-2000 Hz

#### **audio.enabled** (boolean)
- Default: `true`
- Enable/disable audio countdown
- Set to `false` for silent operation

#### **plot.initial_scale** (float)
- Default: `0.0001`
- Initial y-axis maximum
- Auto-expands if data exceeds
- Scientific notation: 1e-4 = 0.0001

#### **plot.scale_padding** (float)
- Default: `1.2`
- Scale expansion multiplier
- 1.2 = 20% padding when auto-scaling

#### **viscosity_labels** (array)
- Default: `["A", "B", "C"]`
- Condition names
- Can use any labels (e.g., ["Low", "Med", "High"])
- Must match number of channels

### Editing Configuration

1. Open `viscosity_config.json` in text editor
2. Modify desired values
3. Save file
4. Restart program to apply changes

**Note**: If config file is missing, default values are used and a new config file is created automatically.

---

## User Interface

### Window Layout

```
┌──────────────────────────────────────────────────────────────┐
│ PhidgetBridge — Syringe Study V3.1 (Participant: 6)         │
├──────────────────────────────────────────────────────────────┤
│ Participant: 6    Trial: 3    Viscosity: B (CH1) - 2/5      │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────┐  │
│  │                                                        │  │
│  │              Real-time Sensor Data                     │  │
│  │         [Live plot of calibrated readings]            │  │
│  │                                                        │  │
│  │  Y-axis: Calibrated Voltage Ratio (0 - 0.0001)       │  │
│  │  X-axis: Sample Number                                │  │
│  │                                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│               Status: Recording Viscosity B (CH1)...         │
│                                                              │
│  [Start Trial]  [Pause]        [Recalibrate]  [Save Data]  │
│                                                              │
│                      Select Viscosity: [A] [B] [C]          │
└──────────────────────────────────────────────────────────────┘
```

### Components

#### **Title Bar**
- Shows software name and version
- Displays current participant ID

#### **Info Panel** (Top)
- **Participant**: Current participant ID
- **Trial**: Current trial number (cumulative)
- **Viscosity**: Current condition, channel, and progress (e.g., "B (CH1) - 2/5")

#### **Plot Area** (Center)
- Real-time data visualization
- Blue line shows calibrated readings
- Auto-scales vertically as needed
- Resets for each new trial

#### **Status Bar** (Below plot)
- Shows current system state
- Updates in real-time
- Examples:
  - "Status: Ready"
  - "Status: Recording Viscosity B (CH1)..."
  - "Status: PAUSED - Viscosity B (CH1)"

#### **Control Buttons**

**Left Side (Trial Control):**
- **Start Trial**: Begin new trial with countdown
  - Transforms to "Stop Trial" during recording
- **Pause**: Pause data collection during trial
  - Transforms to "Continue" when paused
  - Disabled when not recording

**Right Side (Utility):**
- **Recalibrate**: Redo sensor calibration
  - Opens calibration window
  - Disabled during trials
- **Save Data**: Export all data to CSV
  - Can be used anytime
  - Shows save confirmation

**Bottom (Condition Selection):**
- **Viscosity Buttons**: A (CH0), B (CH1), C (CH2)
  - Select condition manually
  - Shows channel mapping
  - Disabled during trials
  - Auto-selects based on counterbalancing

---

## Workflow

### Complete Experiment Workflow

#### **1. Startup**
```
[Program Start]
    ↓
[Enter Participant ID] → ID: 6
    ↓
[Connect to Phidgets] → 3 channels found
    ↓
[Calibration] → 5 seconds zero-point
    ↓
[Main Window Opens]
```

#### **2. Counterbalancing**
Program automatically determines order based on participant ID:

| Participant | Order |
|-------------|-------|
| 1, 7, 13... | A, B, C |
| 2, 8, 14... | A, C, B |
| 3, 9, 15... | B, A, C |
| 4, 10, 16...| B, C, A |
| 5, 11, 17...| C, A, B |
| 6, 12, 18...| C, B, A |

Example: Participant 6 → Order: C, B, A

#### **3. Trial Sequence**

**First Condition (e.g., C):**
```
Trial 1:  [Start Trial] → Countdown → Record → [Stop Trial]
Trial 2:  [Start Trial] → Countdown → Record → [Stop Trial]
Trial 3:  [Start Trial] → Countdown → Record → [Stop Trial]
Trial 4:  [Start Trial] → Countdown → Record → [Stop Trial]
Trial 5:  [Start Trial] → Countdown → Record → [Stop Trial]
    ↓
[Auto-switch to B]
```

**Second Condition (B):**
```
Trial 6:  [Start Trial] → Countdown → Record → [Stop Trial]
Trial 7:  [Start Trial] → Countdown → Record → [Stop Trial]
...
Trial 10: [Start Trial] → Countdown → Record → [Stop Trial]
    ↓
[Auto-switch to A]
```

**Third Condition (A):**
```
Trial 11: [Start Trial] → Countdown → Record → [Stop Trial]
...
Trial 15: [Start Trial] → Countdown → Record → [Stop Trial]
    ↓
[Experiment Complete Dialog]
```

#### **4. During Trial**

**Normal Flow:**
```
Click [Start Trial]
    ↓
Countdown (2 sec beeps)
    ↓
Button becomes [Stop Trial]
[Pause] button enabled
    ↓
Recording... (collect data)
    ↓
Click [Stop Trial]
    ↓
Trial ends
Data saved to memory
Auto-advance after 0.5 sec
```

**With Pause:**
```
Recording...
    ↓
Click [Pause]
    ↓
Data collection pauses
Button becomes [Continue]
Timer paused
    ↓
Click [Continue]
    ↓
Recording resumes
Button becomes [Pause]
Timer resumes
    ↓
Click [Stop Trial]
    ↓
Trial ends
(Pause time excluded from timestamps)
```

#### **5. Completion**

**When all trials done:**
```
[Experiment Complete Dialog]
    ┌─────────────────────────────────┐
    │ 🎉 All trials completed!        │
    │                                 │
    │ Total trials: 15                │
    │ C: 5 trials                     │
    │ B: 5 trials                     │
    │ A: 5 trials                     │
    │                                 │
    │ Continue with more trials?      │
    │                                 │
    │      [Yes]        [No]          │
    └─────────────────────────────────┘
```

**If Yes:** Continue experiment (can do more trials)
**If No:** Prompts to save, then exits

#### **6. Data Export**

**Manual Save:**
```
Click [Save Data]
    ↓
CSV file created
Filename: viscosity_data_6_20250124_153045.csv
    ↓
Confirmation dialog
    ↓
Ready for more trials
```

**Auto-Save on Exit:**
```
Close window
    ↓
Check for unsaved data
    ↓
If data exists: Save automatically
Filename: viscosity_data_6_20250124_153050.csv
    ↓
Exit program
```

---

## Data Output

### Output Files

#### **1. Data File**
**Filename**: `viscosity_data_[ID]_[TIMESTAMP].csv`

**Example**: `viscosity_data_6_20250124_153045.csv`

**Format**: CSV (Comma-Separated Values)

#### **2. Calibration File**
**Filename**: `phidget_calibration_[ID].csv`

**Example**: `phidget_calibration_6.csv`

**Format**: CSV with channel offsets

### Data File Structure

#### **Metadata Header** (First 5 lines)
```csv
# Participant ID:, 6
# Counterbalancing Order:, C, B, A
# Bridge Gain:, 128
# Sampling Frequency (Hz):, 20
# Force Calibration Factor:, 1841.0, N/(V/V)

```

#### **Data Columns**
```csv
Trial,Viscosity,Channel,Gain,Timestamp,Raw_Reading,Calibrated_Reading,Force_N
```

#### **Column Descriptions**

| Column | Description | Units | Example |
|--------|-------------|-------|---------|
| Trial | Trial number (cumulative) | - | 1, 2, 3... |
| Viscosity | Condition label | - | A, B, C |
| Channel | Hardware channel | - | 0, 1, 2 |
| Gain | Bridge gain setting | x | 128 |
| Timestamp | Time from trial start | seconds | 0.0, 0.05, 0.10 |
| Raw_Reading | Raw voltage ratio | V/V | 0.00050406 |
| Calibrated_Reading | Zero-corrected reading | V/V | -0.00003393 |
| Force_N | Calculated force | Newtons | -0.0624525 |

### Example Data

```csv
# Participant ID:, 6
# Counterbalancing Order:, C, B, A
# Bridge Gain:, 128
# Sampling Frequency (Hz):, 20
# Force Calibration Factor:, 1841.0, N/(V/V)

Trial,Viscosity,Channel,Gain,Timestamp,Raw_Reading,Calibrated_Reading,Force_N
1,C,2,128,0.0,0.00050406,-0.00003393,-0.0624525
1,C,2,128,0.05,0.00051234,-0.00002565,-0.0472165
1,C,2,128,0.10,0.00052156,-0.00001643,-0.0302363
1,C,2,128,0.15,0.00053078,-0.00000721,-0.0132661
1,C,2,128,0.20,0.00054001,0.00000202,0.0371882
...
2,C,2,128,0.0,0.00050128,-0.00003671,-0.0675771
2,C,2,128,0.05,0.00051089,-0.00002710,-0.0498971
...
```

### Data Interpretation

#### **Timestamp**
- Starts at 0.0 for each trial
- Increments by sampling interval (e.g., 0.05s at 20 Hz)
- Excludes pause time (only active recording)

#### **Raw_Reading**
- Direct voltage ratio from sensor
- Before calibration correction
- Includes zero offset

#### **Calibrated_Reading**
- Zero-corrected value
- = Raw_Reading - Calibration_Offset
- Negative values = compression
- Positive values = tension

#### **Force_N**
- Calculated force in Newtons
- = Calibrated_Reading × 1841.0
- Based on calibration factor
- Can be negative (directional)

### Calibration File Structure

**Example**: `phidget_calibration_6.csv`

```csv
Channel,Offset
0,0.00053799
1,0.00033799
2,0.00050199
```

- One offset per channel
- Applied to all readings
- Reusable across sessions
- Participant-specific

---

## Features

### 1. Automatic Counterbalancing

**Purpose**: Eliminate order effects in experiments

**How it works**:
- Based on participant ID
- Cycles through all 6 permutations of 3 conditions
- Automatic condition ordering

**Example**:
```
Participant 1: A → B → C
Participant 2: A → C → B
Participant 3: B → A → C
Participant 4: B → C → A
Participant 5: C → A → B
Participant 6: C → B → A
Participant 7: A → B → C (cycles back)
```

**Benefits**:
- ✅ Balanced design
- ✅ Controls for order effects
- ✅ Automatic - no manual selection needed
- ✅ Documented in data file

### 2. Real-Time Visualization

**Features**:
- Live data plotting during trials
- Auto-scaling y-axis (expands only)
- Resets for each trial
- Blue line, 2-pixel width

**Display**:
- X-axis: Sample number
- Y-axis: Calibrated voltage ratio (V/V)
- Title: "Real-time Sensor Data"
- Grid: Yes (30% transparency)

**Scale Behavior**:
```
Initial: 0 to 0.0001
If data > 0.0001: Scale expands to accommodate
New scale = max_value × 1.2 (20% padding)
Per trial: Resets to initial scale
```

### 3. Bridge Gain Control

**Purpose**: Amplify small signals from strain gauges

**Available Gains**: 1, 2, 4, 8, 16, 32, 64, 128

**Configuration**:
```json
{
    "bridge_gain": 128
}
```

**Effect on Range**:
| Gain | Range (mV/V) |
|------|-------------|
| 1 | ±1000 |
| 8 | ±125 |
| 64 | ±15.625 |
| 128 | ±7.8125 |

**Selection Guide**:
- **High (64, 128)**: Small forces, high precision
- **Medium (8-32)**: General purpose
- **Low (1-4)**: Large forces, avoid saturation

### 4. Pause/Resume Functionality

**Purpose**: Pause data collection without ending trial

**How to use**:
1. During recording, click "Pause"
2. Data collection stops
3. Timer pauses
4. Click "Continue" to resume
5. Data collection resumes
6. Click "Stop Trial" to end

**Features**:
- ✅ Pause time excluded from timestamps
- ✅ Can pause multiple times per trial
- ✅ Total pause time tracked
- ✅ Can stop trial while paused

**Use cases**:
- Sensor adjustment needed
- Unexpected interruption
- Multi-phase measurements

### 5. Audio Countdown

**Purpose**: Signal trial start, allow preparation time

**How it works**:
```
Click [Start Trial]
    ↓
Beep 1 (800 Hz, 200ms)
Pause (400ms)
Beep 2 (800 Hz, 200ms)
Pause (400ms)
Beep 3 (800 Hz, 200ms)
Pause (400ms)
Beep 4 (800 Hz, 200ms)
    ↓
Recording starts
```

**Configuration**:
```json
{
    "countdown_duration": 2.0,
    "audio": {
        "frequency": 800,
        "enabled": true
    }
}
```

**Disable Audio**:
Set `"enabled": false` in config file

### 6. Automatic Trial Progression

**Purpose**: Streamline data collection

**How it works**:
1. Trial ends (user clicks Stop)
2. Trial counter increments
3. 0.5 second delay
4. Next trial setup
5. Check if viscosity complete
6. If yes: Auto-switch to next viscosity
7. If all complete: Show completion dialog

**Progress Tracking**:
```
Display: "Viscosity: B (CH1) - 2/5"
         Current condition, channel, progress
```

**Completion**:
```
When all trials done:
- Show dialog with summary
- Option to continue or end
- Prompt to save if not already saved
```

### 7. Calibration System

**Purpose**: Zero-point baseline correction

**Process**:
```
1. Sensors should be unloaded (no force)
2. 5-second data collection
3. Calculate average per channel
4. Store as offset
5. Subtract offset from all readings
```

**Formula**:
```
Calibrated_Reading = Raw_Reading - Offset
```

**When to calibrate**:
- ✅ At experiment start
- ✅ If zero drift detected
- ✅ After hardware changes
- ✅ When prompted

**Recalibration**:
- Available anytime (not during trial)
- Click "Recalibrate" button
- New calibration window opens
- Old calibration replaced

### 8. Force Calculation

**Purpose**: Convert voltage ratios to force (Newtons)

**Formula**:
```
Force (N) = Calibrated_Reading (V/V) × 1841.0
```

**Calibration Factor**: 1841.0 N/(V/V)
- Based on load cell specifications
- Can be changed by editing code
- See FORCE_CALIBRATION_GUIDE.md

**Output**:
- Included in every data row
- Column: Force_N
- Units: Newtons
- Can be negative (compression vs tension)

### 9. Simulation Mode

**Purpose**: Test software without hardware

**Activation**:
- Automatic if no Phidgets detected
- User prompted to enable
- Generates realistic random data

**Simulated Data**:
```python
Base values:
- Channel 0 (A): 0.5 ± 0.05
- Channel 1 (B): 0.3 ± 0.05
- Channel 2 (C): 0.7 ± 0.05
```

**Indicators**:
- Window title: "[SIMULATION]"
- Console: "Running in SIMULATION MODE"

**Limitations**:
- No real sensor data
- No actual gain control
- For testing only

### 10. Data Safety

**Auto-Save on Exit**:
```
Close window
    ↓
Check for unsaved data
    ↓
If found: Automatically save
Confirmation in console
    ↓
Safe to exit
```

**Manual Save**:
- Click "Save Data" anytime
- Creates timestamped file
- Confirmation dialog
- Can save multiple times

**Save Flag**:
- Prevents duplicate auto-save
- Reset on program restart
- Tracked in memory

---

## Troubleshooting

### Common Issues

#### **Issue: No Phidgets Detected**

**Symptoms**:
- Dialog: "No Phidget channels were detected"
- Offered simulation mode

**Solutions**:
1. ✅ Check USB connection
2. ✅ Install Phidget22 drivers
3. ✅ Restart computer
4. ✅ Try different USB port
5. ✅ Check Windows Device Manager (Phidgets section)
6. ✅ Test with Phidget Control Panel software

**Prevention**:
- Use quality USB cable
- Avoid USB hubs if possible
- Update drivers regularly

---

#### **Issue: Audio Not Working**

**Symptoms**:
- No countdown beeps
- Visual countdown only

**Solutions**:
1. ✅ Check system volume
2. ✅ Unmute computer
3. ✅ Check audio output device
4. ✅ Install `winsound` (Windows) or `pygame`
5. ✅ Disable audio in config if not needed

**Config Option**:
```json
{
    "audio": {
        "enabled": false
    }
}
```

---

#### **Issue: Import Error**

**Symptoms**:
```
ModuleNotFoundError: No module named 'Phidget22'
```

**Solutions**:
```bash
pip install Phidget22
pip install matplotlib
pip install customtkinter
```

**Check Installation**:
```bash
python -c "import Phidget22; print('OK')"
```

---

#### **Issue: Config File Not Found**

**Symptoms**:
- Warning: "Config file 'viscosity_config.json' not found"
- "Using default values"

**Solutions**:
- ✅ File auto-created with defaults
- ✅ Check same directory as Python file
- ✅ Edit auto-created file if needed

**Not an error**: Program works with defaults

---

#### **Issue: Calibration Failed**

**Symptoms**:
- Calibration window closes without values
- "Calibration cancelled"

**Solutions**:
1. ✅ Don't touch sensors during calibration
2. ✅ Remove all loads/forces
3. ✅ Wait full 5 seconds
4. ✅ Click "Complete Calibration"
5. ✅ Don't close window early

**Retry**: Click "Recalibrate" button

---

#### **Issue: Data Not Saving**

**Symptoms**:
- No CSV file created
- Save dialog doesn't appear

**Solutions**:
1. ✅ Check write permissions in folder
2. ✅ Check disk space
3. ✅ Run as administrator (Windows)
4. ✅ Check console for error messages
5. ✅ Use different save location

**Auto-Save**: Always attempts on exit

---

#### **Issue: Plot Not Updating**

**Symptoms**:
- Flat line during trial
- No live data

**Solutions**:
1. ✅ Check sensor connection
2. ✅ Verify calibration completed
3. ✅ Check correct channel selected
4. ✅ Restart program
5. ✅ Try different sensor/channel

**Test**: Use simulation mode to verify software

---

#### **Issue: Wrong Channel Selected**

**Symptoms**:
- Reading from incorrect sensor
- Unexpected data

**Solutions**:
1. ✅ Check viscosity-to-channel mapping
2. ✅ Verify physical connections match config
3. ✅ Use viscosity selector buttons
4. ✅ Check console for channel info

**Channel Mapping**:
```
Viscosity A → Channel 0
Viscosity B → Channel 1
Viscosity C → Channel 2
```

---

#### **Issue: Program Crashes**

**Symptoms**:
- Unexpected exit
- Error dialog

**Solutions**:
1. ✅ Check console for error messages
2. ✅ Update Python and libraries
3. ✅ Check for corrupt config file
4. ✅ Delete config file (will regenerate)
5. ✅ Run in simulation mode to isolate hardware issues

**Report Bugs**: Save console output

---

### Error Messages

#### **"Channel X not found or unavailable"**
- **Meaning**: Phidget channel not detected
- **Solution**: Check hardware connections

#### **"Trial Active - Please stop current trial"**
- **Meaning**: Attempted action during recording
- **Solution**: Click "Stop Trial" first

#### **"Failed to save data: [error]"**
- **Meaning**: File write error
- **Solution**: Check permissions and disk space

#### **"Error reading from channel X"**
- **Meaning**: Hardware communication error
- **Solution**: Check USB connection, restart program

---

## Technical Details

### Software Architecture

#### **Main Components**

1. **ParticipantDialog**
   - Get participant ID
   - Validate input
   - Return to main

2. **CalibrationScreen**
   - Zero-point calibration
   - Multi-channel support
   - Average calculation

3. **PhidgetViscosityGUI**
   - Main application window
   - Data collection
   - Real-time plotting
   - User controls

#### **Key Classes**

```python
class ParticipantDialog(CTk):
    """Dialog to enter participant ID"""
    
class CalibrationScreen(CTk):
    """Calibration interface"""
    
class PhidgetViscosityGUI(CTk):
    """Main data collection interface"""
```

### Data Flow

```
[Phidget Hardware]
        ↓
    getVoltageRatio()
        ↓
    Raw Reading (V/V)
        ↓
    Apply Calibration Offset
        ↓
    Calibrated Reading (V/V)
        ↓
    Calculate Force (N)
        ↓
    Store in Memory
        ↓
    Update Plot
        ↓
    Save to CSV
```

### Threading Model

**Main Thread**:
- GUI updates
- User input
- Plot rendering

**Background Thread**:
- Data collection loop
- Audio countdown
- Phidget communication

**Thread Safety**:
- Use `self.after()` for GUI updates from threads
- Shared variables protected by trial_active flag

### Timing

**Sampling Interval**:
```python
interval = 1.0 / sampling_frequency
time.sleep(interval)
```

**At 20 Hz**: 0.05 second intervals
**At 100 Hz**: 0.01 second intervals

**Timestamp Calculation**:
```python
relative_time = time.time() - trial_start_time - total_pause_duration
```

### Memory Usage

**Per Data Point**: ~150 bytes
**1000 samples**: ~150 KB
**Typical trial (10 sec @ 20 Hz)**: ~30 KB
**Full experiment (15 trials)**: ~450 KB

**Plot Memory**: ~5-10 MB (matplotlib overhead)
**Total**: ~20-30 MB typical

### File I/O

**Config Loading**:
- JSON parsing
- Deep merge with defaults
- Validation

**Data Saving**:
- CSV format
- Buffered writing
- Metadata header
- Error handling

**Calibration**:
- CSV format
- Per-participant files
- Reloadable

---

## File Reference

### Primary Files

#### **phidget_viscosity_final.py**
- Main program file
- All functionality included
- ~1600 lines
- Python 3.7+ required

#### **viscosity_config.json**
- Configuration file
- JSON format
- Auto-created if missing
- Edit with text editor

### Documentation Files

#### **QUICK_START.md**
- Getting started guide
- Installation steps
- First run walkthrough

#### **CONFIG_README.md**
- Complete configuration guide
- Parameter descriptions
- Examples

#### **BUTTON_BEHAVIOR.md**
- UI button behavior
- State transitions
- Visual guide

#### **FORCE_CALIBRATION_GUIDE.md**
- Force conversion details
- Calibration procedures
- Post-processing examples

#### **GAIN_IMPLEMENTATION.md**
- Bridge gain feature
- Technical details
- Configuration

#### **GUI_LAYOUT_UPDATE.md**
- UI design documentation
- Layout changes
- Visual reference

### Output Files

#### **viscosity_data_[ID]_[TIMESTAMP].csv**
- Experimental data
- CSV format
- Includes metadata
- One per save

**Example**: `viscosity_data_6_20250124_153045.csv`

#### **phidget_calibration_[ID].csv**
- Calibration offsets
- CSV format
- One per participant
- Reusable

**Example**: `phidget_calibration_6.csv`

### File Organization

```
project_folder/
│
├── phidget_viscosity_final.py          # Main program
├── viscosity_config.json               # Configuration
│
├── Documentation/
│   ├── QUICK_START.md
│   ├── CONFIG_README.md
│   ├── BUTTON_BEHAVIOR.md
│   ├── FORCE_CALIBRATION_GUIDE.md
│   ├── GAIN_IMPLEMENTATION.md
│   └── GUI_LAYOUT_UPDATE.md
│
└── Data/                               # Output files
    ├── viscosity_data_6_20250124_153045.csv
    ├── viscosity_data_7_20250124_160230.csv
    ├── phidget_calibration_6.csv
    └── phidget_calibration_7.csv
```

---

## Appendix

### A. Keyboard Shortcuts

Currently no keyboard shortcuts implemented.
All control via mouse/touch.

### B. Command Line Options

No command line arguments currently supported.
Run with: `python phidget_viscosity_final.py`

### C. Version History

**V3.1** (October 2024)
- Force calculation added
- Gain parameter in output
- Counterbalancing in metadata
- Improved button layout
- Larger window size

**V3.0** (Earlier)
- Pause/resume functionality
- Auto trial progression
- Enhanced GUI
- Config file system

**V2.x** (Earlier)
- Calibration system
- Multi-channel support
- Real-time plotting

**V1.x** (Earlier)
- Basic data collection
- Single channel

### D. Known Limitations

1. **Maximum Channels**: 4 (hardware limit)
2. **Maximum Sampling Rate**: ~200 Hz (practical limit)
3. **File Format**: CSV only (no binary formats)
4. **Plot History**: Current trial only (not cumulative)
5. **Gain Changes**: Requires reconnection

### E. Future Enhancements

**Possible Features**:
- [ ] Keyboard shortcuts
- [ ] Export to Excel format
- [ ] Real-time force display
- [ ] Multiple plot views
- [ ] Custom condition names in UI
- [ ] Data analysis tools
- [ ] Automatic backup
- [ ] Network data sync
- [ ] Advanced statistics

### F. Support

**For Issues**:
1. Check this documentation
2. Review console output
3. Try simulation mode
4. Update software and drivers

**Contact Information**:
See project README or contact project lead.

### G. License

See project LICENSE file for details.

### H. Credits

**Software Development**: [Project Team]
**Hardware**: Phidgets Inc.
**Libraries**: Python community

---

## Summary

This software provides a complete solution for multi-channel force/viscosity measurement with:

✅ Automated data collection
✅ Real-time visualization
✅ Counterbalanced experimental design
✅ Configurable parameters
✅ Professional data output
✅ User-friendly interface
✅ Robust error handling
✅ Comprehensive documentation

**For Questions**: Refer to specific documentation files or troubleshooting section.

**Ready to Start**: See [Quick Start](#quick-start) section.

---

*End of Documentation*
