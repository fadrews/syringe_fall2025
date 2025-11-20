# GUI Layout Changes

## New Button Organization

### Visual Layout:

```
┌─────────────────────────────────────────────────────────────────┐
│ Participant: 6    Trial: 3    Viscosity: B (CH1) - 2/5         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│                      [PLOT AREA]                                 │
│                   Real-time Sensor Data                          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

                     Status: Ready

┌───────────────────────────────┐   ║   ┌─────────────────────────┐
│ LEFT: Trial Control           │   ║   │ RIGHT: Other Controls   │
│  ┌─────────────────────────┐  │   ║   │  ┌──────────────────┐   │
│  │    Start Trial          │  │   ║   │  │  Recalibrate     │   │
│  └─────────────────────────┘  │   ║   │  └──────────────────┘   │
│  ┌─────────────────────────┐  │   ║   │  ┌──────────────────┐   │
│  │    Stop Trial           │  │   ║   │  │  Save Data       │   │
│  │   (GREEN when active)   │  │   ║   │  └──────────────────┘   │
│  └─────────────────────────┘  │   ║   │                         │
└───────────────────────────────┘   ║   └─────────────────────────┘
                                    SEPARATOR

                                            Select Viscosity: [A] [B] [C]
```

## Changes Made

### 1. **Button Layout**

**BEFORE:**
```
[Start Trial] [Stop Trial] [Recalibrate] [Save Data]
              (all in one row)
```

**AFTER:**
```
LEFT                    SEPARATOR    RIGHT
[Start Trial]              ║         [Recalibrate]
[Stop Trial]               ║         [Save Data]
```

### 2. **Viscosity Selector**
- Moved to **bottom right** (aligned with right buttons)
- Still horizontal layout
- Keeps label: "Select Viscosity:"

### 3. **Stop Trial Button Color**

**When Trial is NOT Running:**
- Text color: Default (gray/white depending on theme)
- State: Disabled

**When Trial IS Running:**
- Text color: **GREEN** 🟢
- State: Enabled
- Clear visual indicator that recording is active

**Code:**
```python
# When trial starts:
self.btn_stop.configure(state="normal", text_color="green")

# When trial stops:
self.btn_stop.configure(state="disabled", text_color=("gray10", "gray90"))
```

### 4. **Visual Separator**
- Vertical gray line between left and right sections
- 2 pixels wide
- Spans button height
- 20px padding on each side

## Benefits

✅ **Clearer Organization**: Trial controls separate from utility buttons
✅ **Visual Indicator**: Green text shows when recording is active
✅ **Better Workflow**: Most-used buttons (Start/Stop) grouped together
✅ **Less Clutter**: Separator helps visual grouping
✅ **Intuitive**: Left = trial control, Right = other functions

## Button Groups

### Left Side (Trial Control)
1. **Start Trial / Pause** - Begin or pause data collection
2. **Stop Trial** - End current trial (GREEN when active)

### Right Side (Utility)
1. **Recalibrate** - Redo sensor calibration
2. **Save Data** - Export all data to CSV

### Bottom Right
- **Viscosity Selector** - A (CH0), B (CH1), C (CH2)

## Color Indicators

| Button State | Text Color | Meaning |
|--------------|------------|---------|
| Start Trial (Ready) | Default | Ready to begin |
| Pause (Active) | Default | Trial running, can pause |
| Stop Trial (Disabled) | Gray | No trial running |
| Stop Trial (Active) | **GREEN** 🟢 | Recording - click to stop |

## Usage Flow

1. **Before Trial**: All buttons default color
2. **Click Start**: Countdown begins
3. **Recording Starts**: Stop button turns GREEN
4. **User Action**: See green → know to click when done
5. **Click Stop**: GREEN → back to default gray
6. **Auto-advance**: Next trial or viscosity

The green color makes it immediately obvious that:
- ✅ Trial is actively recording
- ✅ This is the button to click to stop
- ✅ Data is being collected right now
