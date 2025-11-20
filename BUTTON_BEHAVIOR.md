# Updated Button Layout and Behavior

## New Button Organization

### Visual Layout:

```
┌───────────────────────────────────────────────────────────────┐
│                                                                 │
│                       [PLOT AREA]                              │
│                                                                 │
└───────────────────────────────────────────────────────────────┘

                    Status: Ready

LEFT SIDE                          RIGHT SIDE
─────────────────────             ─────────────────────
[Start Trial]    [Pause]          [Recalibrate] [Save Data]
                 (disabled)

                                   Select Viscosity: [A] [B] [C]
```

## Button State Flow

### **State 1: Before Trial (Ready)**
```
[Start Trial]    [Pause]          [Recalibrate] [Save Data]
   (enabled)     (disabled)
```

**User clicks "Start Trial"** → Countdown begins...

---

### **State 2: During Trial (Recording)**
```
[Stop Trial]     [Pause]          [Recalibrate] [Save Data]
   (enabled)     (enabled)
```

**Button Transformations:**
- ✅ **[Start Trial]** → **[Stop Trial]** (same button, text + function changed)
- ✅ **[Pause]** → **enabled** (ready to pause recording)

**User can now:**
- Click **Stop Trial** → End trial
- Click **Pause** → Pause recording

---

### **State 3: Paused (During Trial)**
```
[Stop Trial]     [Continue]       [Recalibrate] [Save Data]
   (enabled)     (enabled)
```

**Button Changes:**
- **[Pause]** → **[Continue]** (same button, text changed)

**User can:**
- Click **Stop Trial** → End trial (even while paused)
- Click **Continue** → Resume recording

**User clicks "Continue"** → Returns to State 2

---

### **State 4: Trial Stopped**
```
[Start Trial]    [Pause]          [Recalibrate] [Save Data]
   (enabled)     (disabled)
```

**Automatic Reset:**
- **[Stop Trial]** → **[Start Trial]** (back to original)
- **[Pause/Continue]** → **[Pause]** (disabled)

---

## Button Behavior Summary

### **Left Button (btn_start)**

| State | Text | Function | Status |
|-------|------|----------|--------|
| Ready | Start Trial | start_trial() | Enabled |
| Countdown | Start Trial | - | Disabled |
| Recording | **Stop Trial** | stop_trial() | Enabled |
| Stopped | Start Trial | start_trial() | Enabled |

### **Right Button (btn_pause)**

| State | Text | Function | Status |
|-------|------|----------|--------|
| Ready | Pause | toggle_pause() | Disabled |
| Countdown | Pause | toggle_pause() | Disabled |
| Recording | Pause | toggle_pause() | Enabled |
| Paused | **Continue** | toggle_pause() | Enabled |
| Stopped | Pause | toggle_pause() | Disabled |

## Key Features

✅ **Single Start/Stop Button**: 
   - Starts as "Start Trial"
   - Becomes "Stop Trial" during recording
   - No separate stop button needed

✅ **Pause Button Always in Same Place**:
   - Second position (where old Stop button was)
   - Toggles between "Pause" and "Continue"
   - Only active during trials

✅ **Clear Visual Flow**:
   - Left button = main action (start → stop)
   - Right button = secondary action (pause/continue)

✅ **Intuitive**:
   - "Start" becomes "Stop" (opposite action)
   - "Pause" becomes "Continue" (opposite action)

## Usage Example

1. **Start Trial**: Click [Start Trial]
2. **Countdown**: 2 second beeps (both buttons disabled)
3. **Recording**: Button changes to [Stop Trial], [Pause] enabled
4. **Optional Pause**: Click [Pause] → becomes [Continue]
5. **Optional Resume**: Click [Continue] → becomes [Pause]
6. **End Trial**: Click [Stop Trial]
7. **Ready for Next**: Button resets to [Start Trial]

## Technical Implementation

### Button Creation:
```python
# Left button: Start/Stop
self.btn_start = CTkButton(
    text="Start Trial",
    command=self.start_trial
)

# Right button: Pause/Continue
self.btn_pause = CTkButton(
    text="Pause",
    command=self.toggle_pause,
    state="disabled"
)
```

### When Trial Starts:
```python
# Transform Start → Stop
self.btn_start.configure(
    text="Stop Trial",
    command=self.stop_trial,
    state="normal"
)

# Enable Pause
self.btn_pause.configure(state="normal")
```

### When Pause Clicked:
```python
# Transform Pause → Continue
self.btn_pause.configure(text="Continue")
```

### When Continue Clicked:
```python
# Transform Continue → Pause
self.btn_pause.configure(text="Pause")
```

### When Trial Stops:
```python
# Reset Stop → Start
self.btn_start.configure(
    text="Start Trial",
    command=self.start_trial,
    state="normal"
)

# Disable and reset Pause
self.btn_pause.configure(
    text="Pause",
    state="disabled"
)
```

## Benefits

✅ **Cleaner Interface**: One less button visible
✅ **Logical Flow**: Start becomes Stop (natural opposite)
✅ **Space Efficient**: Pause button in consistent location
✅ **User Friendly**: Button text always shows current action
✅ **No Confusion**: Can't accidentally click wrong button
