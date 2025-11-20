# Documentation Index
## Phidget Viscosity Measurement System V3.1

---

## 📚 Documentation Files

### **Primary Documentation**

#### [COMPLETE_DOCUMENTATION.md](COMPLETE_DOCUMENTATION.md) ⭐ START HERE
**Comprehensive software manual** covering everything:
- Installation and setup
- Complete feature descriptions
- User interface guide
- Workflow instructions
- Troubleshooting
- Technical details
- 100+ pages of detailed information

---

### **Quick Reference Guides**

#### [QUICK_START.md](QUICK_START.md)
**Get running in 5 minutes**
- Installation steps
- First run workflow
- Basic usage
- Quick tips

#### [CONFIG_README.md](CONFIG_README.md)
**Configuration guide**
- All parameters explained
- Default values
- Examples
- How to edit settings

---

### **Feature-Specific Guides**

#### [BUTTON_BEHAVIOR.md](BUTTON_BEHAVIOR.md)
**UI button reference**
- Button states and transitions
- Visual flow diagrams
- Usage examples

#### [FORCE_CALIBRATION_GUIDE.md](FORCE_CALIBRATION_GUIDE.md)
**Converting to Newtons**
- Calibration procedures
- Force calculation methods
- Post-processing examples
- Python/Excel scripts

#### [GAIN_IMPLEMENTATION.md](GAIN_IMPLEMENTATION.md)
**Bridge gain feature**
- How gain works
- Configuration
- Selection guide
- Technical details

#### [GUI_LAYOUT_UPDATE.md](GUI_LAYOUT_UPDATE.md)
**Interface design**
- Layout organization
- Visual references
- Button placement

---

## 🚀 Getting Started Path

### For First-Time Users:
```
1. Read: QUICK_START.md (5 min)
2. Install Python & libraries
3. Run program
4. If issues: See COMPLETE_DOCUMENTATION.md → Troubleshooting
```

### For Configuration:
```
1. Read: CONFIG_README.md
2. Edit: viscosity_config.json
3. Restart program
```

### For Understanding Features:
```
Read: COMPLETE_DOCUMENTATION.md → Features section
```

---

## 📋 Quick Reference

### Essential Information

**Main Program**: `phidget_viscosity_final.py`
**Config File**: `viscosity_config.json`
**Output Format**: CSV with metadata
**Default Window**: 1400 × 900 pixels
**Default Sampling**: 20 Hz
**Default Gain**: 128x

### File Locations

**User Files** (you create):
- Configuration: `viscosity_config.json`

**Program Files** (provided):
- Main program: `phidget_viscosity_final.py`
- Documentation: `*.md` files

**Output Files** (auto-generated):
- Data: `viscosity_data_[ID]_[timestamp].csv`
- Calibration: `phidget_calibration_[ID].csv`

---

## 🎯 Common Tasks

| Task | Documentation | Quick Link |
|------|---------------|------------|
| Install software | QUICK_START.md | → Installation |
| First run | QUICK_START.md | → Workflow |
| Change settings | CONFIG_README.md | → Parameters |
| Understand buttons | BUTTON_BEHAVIOR.md | → States |
| Convert to Newtons | FORCE_CALIBRATION_GUIDE.md | → Conversion |
| Adjust gain | GAIN_IMPLEMENTATION.md | → Configuration |
| Fix problems | COMPLETE_DOCUMENTATION.md | → Troubleshooting |
| Understand output | COMPLETE_DOCUMENTATION.md | → Data Output |
| Learn features | COMPLETE_DOCUMENTATION.md | → Features |

---

## 💡 Quick Tips

### Installation
```bash
pip install Phidget22 matplotlib customtkinter
python phidget_viscosity_final.py
```

### Config File (viscosity_config.json)
```json
{
    "sampling_frequency": 20,
    "trials_per_viscosity": 5,
    "bridge_gain": 128
}
```

### Common Issues
1. **No Phidgets detected?** → Install drivers, check USB
2. **No audio?** → Set `"audio.enabled": false` in config
3. **Wrong scale?** → Edit `"plot.initial_scale"` in config

---

## 📊 Data Output Format

### CSV Structure
```csv
# Participant ID:, 6
# Counterbalancing Order:, C, B, A
# Bridge Gain:, 128

Trial,Viscosity,Channel,Gain,Timestamp,Raw_Reading,Calibrated_Reading,Force_N
1,C,2,128,0.0,0.00050406,-0.00003393,-0.0624525
```

### Columns Explained
- **Trial**: Sequential trial number
- **Viscosity**: Condition (A, B, C)
- **Channel**: Hardware channel (0, 1, 2)
- **Gain**: Bridge amplification (1-128)
- **Timestamp**: Seconds from trial start
- **Raw_Reading**: Raw voltage ratio (V/V)
- **Calibrated_Reading**: Zero-corrected (V/V)
- **Force_N**: Calculated force (Newtons)

---

## 🔧 Configuration Quick Reference

### Most Commonly Changed

```json
{
    "sampling_frequency": 20,          // Samples per second
    "trials_per_viscosity": 5,         // Trials per condition
    "bridge_gain": 128,                // Sensor sensitivity (1-128)
    "plot": {
        "initial_scale": 0.0001        // Y-axis range
    }
}
```

### Audio Settings
```json
{
    "audio": {
        "frequency": 800,              // Beep pitch (Hz)
        "enabled": true                // Turn on/off
    }
}
```

---

## 🎓 Learning Path

### Beginner → Advanced

**Level 1: Basic Usage** (30 min)
1. QUICK_START.md
2. Run first experiment
3. Save data

**Level 2: Customization** (1 hour)
1. CONFIG_README.md
2. Modify settings
3. Understand counterbalancing

**Level 3: Advanced** (2 hours)
1. COMPLETE_DOCUMENTATION.md (full read)
2. FORCE_CALIBRATION_GUIDE.md
3. Custom analysis scripts

**Level 4: Expert** (4+ hours)
1. All documentation
2. Code exploration
3. Advanced features

---

## 📞 Support Resources

### Self-Help (Recommended First)
1. Check relevant documentation file
2. Review troubleshooting section
3. Try simulation mode
4. Check console output

### Documentation Coverage

| Question | Find Answer In |
|----------|---------------|
| How do I install? | QUICK_START.md |
| How do I change X? | CONFIG_README.md |
| What does button Y do? | BUTTON_BEHAVIOR.md |
| How do I convert to force? | FORCE_CALIBRATION_GUIDE.md |
| What is gain? | GAIN_IMPLEMENTATION.md |
| How does the workflow work? | COMPLETE_DOCUMENTATION.md |
| Why doesn't it work? | COMPLETE_DOCUMENTATION.md → Troubleshooting |

---

## 🎯 Use Case Examples

### Basic Experiment
```
1. Start program
2. Enter ID: 1
3. Calibrate
4. Run 15 trials (auto-progression)
5. Save data
```

### Custom Configuration
```
1. Edit viscosity_config.json:
   - Set trials_per_viscosity: 10
   - Set sampling_frequency: 50
2. Restart program
3. Run experiment
```

### Data Analysis
```
1. Collect data (CSV output)
2. Open in Excel/Python/R
3. Use Force_N column
4. Analyze by Viscosity
```

---

## 📦 Complete File List

### Program Files
- `phidget_viscosity_final.py` - Main program (required)
- `viscosity_config.json` - Configuration (auto-created)

### Documentation Files
- `COMPLETE_DOCUMENTATION.md` - Full manual ⭐
- `QUICK_START.md` - Quick guide
- `CONFIG_README.md` - Configuration reference
- `BUTTON_BEHAVIOR.md` - Button guide
- `FORCE_CALIBRATION_GUIDE.md` - Force conversion
- `GAIN_IMPLEMENTATION.md` - Gain feature
- `GUI_LAYOUT_UPDATE.md` - UI design
- `DOCUMENTATION_INDEX.md` - This file

### Output Files (Generated)
- `viscosity_data_*.csv` - Experimental data
- `phidget_calibration_*.csv` - Calibration data

---

## ✅ Checklist

### Before First Use
- [ ] Python installed (3.7+)
- [ ] Libraries installed (Phidget22, matplotlib)
- [ ] Phidget drivers installed
- [ ] Hardware connected
- [ ] Documentation reviewed

### Before Each Session
- [ ] Config file checked
- [ ] Hardware connected
- [ ] Sensors unloaded (for calibration)
- [ ] Data folder ready

### After Each Session
- [ ] Data saved
- [ ] Backup created
- [ ] Equipment stored properly

---

## 🚀 Version Information

**Current Version**: V3.1
**Last Updated**: October 2024
**Python Required**: 3.7+
**Platform**: Windows, macOS, Linux

---

## 📖 Reading Order Recommendations

### Quick Start (15 minutes)
```
1. QUICK_START.md
2. Run program in simulation mode
3. Explore interface
```

### Complete Understanding (2 hours)
```
1. QUICK_START.md
2. CONFIG_README.md
3. COMPLETE_DOCUMENTATION.md (skim)
4. Feature-specific guides (as needed)
```

### Expert Level (4+ hours)
```
1. All documentation files (read fully)
2. Experiment with all features
3. Test different configurations
4. Review code
```

---

## 🎉 You're Ready!

**Next Steps**:
1. Open [QUICK_START.md](QUICK_START.md)
2. Follow installation steps
3. Run your first experiment

**Questions?**
- Check relevant documentation file above
- Review troubleshooting in COMPLETE_DOCUMENTATION.md

**Happy Experimenting! 🔬**

---

*Phidget Viscosity Measurement System V3.1*
