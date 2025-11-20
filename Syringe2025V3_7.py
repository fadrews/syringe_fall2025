# Phidget Viscosity Measurement System - IMPROVED WITH ERROR HANDLING
# CONFIG_README has the information about the configuration
# Phidget_calibration_participantnumber has information about the calibration data
# viscosity_config.json stores configuration
# Working code for phidget with random generated values for testing if phidget not attached
# Requires config file; if not, loads default values
# Includes calibration procedure
# Fixed trial end; now only when user ends trial
# Redraws data window after every trial
# Added comprehensive error handling for file operations and hardware failures
# Phidget Viscosity Measurement System - IMPROVED WITH ERROR HANDLING
# CONFIG_README has the information about the configuration
# Phidget_calibration_participantnumber has information about the calibration data
# viscosity_config.json stores configuration
# Working code for phidget with random generated values for testing if phidget not attached
# Requires config file; if not, loads default values
# Includes calibration procedure
# Fixed trial end; now only when user ends trial
# Redraws data window after every trial
# Added comprehensive error handling for file operations and hardware failures
# Added background auto-save after each trial to main participant file

import os
import csv
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, Toplevel
import sys
import json
import itertools
import queue
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *

# Audio for countdown - try multiple methods
AUDIO_METHOD = None
try:
    if sys.platform == 'win32':
        import winsound

        AUDIO_METHOD = 'winsound'
        print("✅ Using winsound for audio")
except ImportError:
    pass

if AUDIO_METHOD is None:
    try:
        import pygame

        pygame.mixer.init()
        AUDIO_METHOD = 'pygame'
        print("✅ Using pygame for audio")
    except:
        pass

if AUDIO_METHOD is None:
    print("⚠️ No audio library available - using visual countdown only")
    AUDIO_METHOD = 'none'

try:
    from customtkinter import CTk, CTkButton, CTkLabel, CTkFrame, CTkEntry

    USE_CUSTOM_TK = True
except ImportError:
    from tkinter import Tk as CTk, Button as CTkButton, Label as CTkLabel, Frame as CTkFrame, Entry as CTkEntry

    USE_CUSTOM_TK = False

# --- Add Phidget DLL path (Windows only) ---
if os.name == 'nt':  # Windows
    dll_path = r"C:\Program Files\Phidgets\Phidget22"
    if os.path.exists(dll_path):
        os.add_dll_directory(dll_path)

CALIBRATION_FILE = "phidget_calibration.csv"
CONFIG_FILE = "viscosity_config.json"

# OUTPUT_DIR will be set after loading config
OUTPUT_DIR = None

# Default configuration values
DEFAULT_CONFIG = {
    "calibration_duration": 5.0,
    "sampling_frequency": 100,
    "countdown_duration": 2.0,
    "num_channels": 3,
    "trials_per_viscosity": 5,
    "bridge_gain": 128,
    "output_directory": r"C:\Users\Public",  # Default output directory for data files
    "audio": {
        "frequency": 800,
        "enabled": True
    },
    "plot": {
        "initial_scale": 0.0001,
        "scale_padding": 1.2
    },
    "viscosity_labels": ["A", "B", "C"]
}


# ============================================================
# === Helper Functions =======================================
# ============================================================

def is_file_locked(filepath):
    """Check if a file is locked by another process"""
    if not os.path.exists(filepath):
        return False
    try:
        with open(filepath, 'a'):
            return False
    except (PermissionError, IOError):
        return True


def safe_file_write(filepath, write_function, max_attempts=3):
    """
    Safely write to a file with retry logic and error handling.

    Args:
        filepath: Path to the file to write
        write_function: Function that takes a file object and writes to it
        max_attempts: Maximum number of retry attempts

    Returns:
        (success, error_message) tuple
    """
    for attempt in range(max_attempts):
        try:
            # Check if file is locked before attempting
            if os.path.exists(filepath) and is_file_locked(filepath):
                if attempt < max_attempts - 1:
                    print(f"⚠️ File locked, attempt {attempt + 1}/{max_attempts}")
                    time.sleep(0.5)
                    continue
                else:
                    return False, f"File is locked by another program: {filepath}"

            # Attempt to write
            with open(filepath, 'w', newline='') as f:
                write_function(f)

            return True, None

        except PermissionError as e:
            if attempt < max_attempts - 1:
                print(f"⚠️ Permission error, attempt {attempt + 1}/{max_attempts}")
                time.sleep(0.5)
            else:
                return False, f"Permission denied. File may be open in another program: {os.path.basename(filepath)}"

        except IOError as e:
            return False, f"IO Error writing file: {e}"

        except Exception as e:
            return False, f"Unexpected error writing file: {e}"

    return False, "Failed after maximum retry attempts"


# ============================================================
# === Configuration Management ===============================
# ============================================================

def load_config(filename=CONFIG_FILE):
    """
    Load configuration from JSON file with error handling.
    Returns default config if file not found or invalid.
    """
    config = DEFAULT_CONFIG.copy()
    try:
        with open(filename, 'r') as f:
            user_config = json.load(f)
            # Deep merge user config with defaults
            for key, value in user_config.items():
                if isinstance(value, dict) and key in config:
                    config[key].update(value)
                else:
                    config[key] = value
        print(f"✅ Loaded configuration from '{filename}'")
    except FileNotFoundError:
        print(f"⚠️ Config file '{filename}' not found. Creating default configuration.")
        save_config(config, filename)
    except json.JSONDecodeError as e:
        print(f"⚠️ Error parsing config file: {e}. Using default values.")
        # Try to backup the corrupted file
        try:
            backup_name = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(filename, backup_name)
            print(f"⚠️ Corrupted config backed up to: {backup_name}")
        except:
            pass
    except Exception as e:
        print(f"⚠️ Error loading config: {e}. Using default values.")

    # Calculate sampling interval from frequency
    try:
        config['sampling_interval'] = 1.0 / config['sampling_frequency']
    except (KeyError, ZeroDivisionError):
        print("⚠️ Invalid sampling frequency, using default")
        config['sampling_frequency'] = 100
        config['sampling_interval'] = 0.01

    return config


def save_config(config, filename=CONFIG_FILE):
    """Save configuration to JSON file with error handling"""
    try:
        # Remove calculated values before saving
        save_config_data = config.copy()
        save_config_data.pop('sampling_interval', None)

        def write_config(f):
            json.dump(save_config_data, f, indent=4)

        success, error = safe_file_write(filename, write_config)
        if success:
            print(f"💾 Saved configuration to '{filename}'")
        else:
            print(f"⚠️ Error saving config: {error}")

    except Exception as e:
        print(f"⚠️ Unexpected error saving config: {e}")


# Load configuration at startup
CONFIG = load_config()
print(f"📋 Configuration loaded:")
print(f"   Calibration duration: {CONFIG['calibration_duration']}s")
print(f"   Sampling frequency: {CONFIG['sampling_frequency']} Hz")
print(f"   Countdown duration: {CONFIG['countdown_duration']}s")
print(f"   Channels: {CONFIG['num_channels']}")
print(f"   Trials per viscosity: {CONFIG['trials_per_viscosity']}")
print(f"   Bridge gain: {CONFIG['bridge_gain']}x")
print(f"   Viscosity labels: {CONFIG['viscosity_labels']}")
print()

# Initialize output directory from config
OUTPUT_DIR = CONFIG.get('output_directory', r"C:\Users\Public")

# Expand environment variables and user paths (e.g., ~)
OUTPUT_DIR = os.path.expandvars(os.path.expanduser(OUTPUT_DIR))

# Create output directory if it doesn't exist
try:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"✅ Output directory ready: {OUTPUT_DIR}")
except PermissionError:
    print(f"⚠️ Permission denied creating directory: {OUTPUT_DIR}")
    print(f"   Falling back to current directory")
    OUTPUT_DIR = "."
except Exception as e:
    print(f"⚠️ Could not create output directory '{OUTPUT_DIR}': {e}")
    print(f"   Falling back to current directory")
    OUTPUT_DIR = "."

# Verify we can write to the directory
try:
    test_file = os.path.join(OUTPUT_DIR, ".write_test")
    with open(test_file, 'w') as f:
        f.write("test")
    os.remove(test_file)
    print(f"✅ Write access confirmed for: {OUTPUT_DIR}\n")
except Exception as e:
    print(f"⚠️ Cannot write to directory '{OUTPUT_DIR}': {e}")
    print(f"   Falling back to current directory")
    OUTPUT_DIR = "."
    print(f"✅ Using current directory: {os.path.abspath(OUTPUT_DIR)}\n")


# =======================================================
# ============Permutation================================
# =======================================================

def get_counterbalanced_order(participant_id, conditions=None):
    """
    Returns a counterbalanced order for viscosities based on participant ID.
    Cycles through all 6 permutations of conditions.
    """
    if conditions is None:
        conditions = CONFIG['viscosity_labels']

    try:
        permutations = list(itertools.permutations(conditions))

        # Try to extract a numeric participant number from ID
        try:
            p_num = int(''.join(filter(str.isdigit, str(participant_id))))
            if p_num <= 0:
                p_num = 1
        except:
            p_num = 1

        index = (p_num - 1) % len(permutations)
        return list(permutations[index])

    except Exception as e:
        print(f"⚠️ Error calculating counterbalanced order: {e}")
        # Return default order if calculation fails
        return conditions if conditions else ['A', 'B', 'C']


# ============================================================
# === Calibration ============================================
# ============================================================

def load_calibration(filename=CALIBRATION_FILE):
    """Load calibration offsets from CSV file with error handling"""
    calibration = {}
    try:
        with open(filename, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    channel = int(row["Channel"])
                    offset = float(row["Offset (VoltageRatio)"])
                    calibration[channel] = offset
                except (ValueError, KeyError) as e:
                    print(f"⚠️ Skipping invalid calibration row: {e}")

        print(f"✅ Loaded calibration from {filename}")
    except FileNotFoundError:
        print("⚠️ No calibration file found — using zero offsets.")
    except Exception as e:
        print(f"⚠️ Error loading calibration: {e}")
    return calibration


def save_calibration(calibration, participant_id=None, filename=None):
    """Save calibration offsets to CSV file with error handling"""
    if filename is None:
        if participant_id:
            filename = f"phidget_calibration_{participant_id}.csv"
        else:
            filename = CALIBRATION_FILE

    try:
        def write_calibration(f):
            w = csv.DictWriter(f, fieldnames=["Channel", "Offset (VoltageRatio)"])
            w.writeheader()
            for ch, off in calibration.items():
                w.writerow({"Channel": ch, "Offset (VoltageRatio)": off})

        success, error = safe_file_write(filename, write_calibration)
        if success:
            print(f"💾 Saved calibration to {filename}")
        else:
            print(f"⚠️ Error saving calibration: {error}")
            # Show user warning
            try:
                messagebox.showwarning("Calibration Save Warning",
                                       f"Could not save calibration file:\n{error}")
            except:
                pass

    except Exception as e:
        print(f"⚠️ Unexpected error saving calibration: {e}")


# ============================================================
# === Phidget Connection =====================================
# ============================================================

def connect_channels():
    """
    Open channels on the PhidgetBridge with comprehensive error handling.
    Returns a list of active VoltageRatioInput objects.
    """
    active = []
    num_channels = CONFIG['num_channels']
    bridge_gain = CONFIG['bridge_gain']

    print(f"🔌 Connecting to PhidgetBridge channels (0-{num_channels - 1})...")
    print(f"   Setting bridge gain to: {bridge_gain}x")

    for ch_num in range(num_channels):
        try:
            vi = VoltageRatioInput()
            vi.setChannel(ch_num)

            # Attempt to open with timeout
            try:
                vi.openWaitForAttachment(1000)
            except PhidgetException as e:
                print(f"⚠️ Channel {ch_num} not found: {e}")
                continue

            # Set bridge gain from config
            try:
                from Phidget22.BridgeGain import BridgeGain
                gain_map = {
                    1: BridgeGain.BRIDGE_GAIN_1,
                    2: BridgeGain.BRIDGE_GAIN_2,
                    4: BridgeGain.BRIDGE_GAIN_4,
                    8: BridgeGain.BRIDGE_GAIN_8,
                    16: BridgeGain.BRIDGE_GAIN_16,
                    32: BridgeGain.BRIDGE_GAIN_32,
                    64: BridgeGain.BRIDGE_GAIN_64,
                    128: BridgeGain.BRIDGE_GAIN_128
                }

                if bridge_gain in gain_map:
                    vi.setBridgeGain(gain_map[bridge_gain])
                    print(f"✅ Channel {ch_num} attached (gain: {bridge_gain}x)")
                else:
                    print(f"⚠️ Invalid gain {bridge_gain}, using default for channel {ch_num}")
                    print(f"✅ Channel {ch_num} attached (gain: default)")
            except Exception as e:
                print(f"⚠️ Could not set gain for channel {ch_num}: {e}")
                print(f"✅ Channel {ch_num} attached (gain: default)")

            active.append(vi)

        except PhidgetException as e:
            print(f"⚠️ Channel {ch_num} error: {e}")
        except Exception as e:
            print(f"⚠️ Unexpected error connecting channel {ch_num}: {e}")

    if not active:
        print("❌ No channels connected")
        print("   TIP: Check USB connection and ensure Phidget22 drivers are installed")
    else:
        print(f"✅ Total: {len(active)} channel(s) connected successfully\n")

    return active


# ============================================================
# === Participant ID Dialog ==================================
# ============================================================

class ParticipantDialog(CTk):
    def __init__(self):
        super().__init__()
        self.title("Viscosity Measurement System")
        self.geometry("600x400")
        self.participant_id = None

        self.resizable(False, False)

        if USE_CUSTOM_TK:
            self.configure(bg="#1a1a2e")

        main_frame = CTkFrame(self, corner_radius=15)
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        header = CTkLabel(main_frame,
                          text="🔬 Viscosity Measurement System",
                          font=("Arial", 24, "bold"))
        header.pack(pady=(30, 10))

        subtitle = CTkLabel(main_frame,
                            text="PhidgetBridge Data Collection",
                            font=("Arial", 14))
        subtitle.pack(pady=(0, 40))

        input_section = CTkFrame(main_frame, corner_radius=10)
        input_section.pack(pady=20, padx=40, fill="x")

        label = CTkLabel(input_section,
                         text="Participant ID:",
                         font=("Arial", 16))
        label.pack(pady=(20, 10))

        self.entry = CTkEntry(input_section,
                              width=300,
                              height=45,
                              font=("Arial", 16),
                              justify="center")
        self.entry.pack(pady=(10, 20), padx=20)
        self.entry.focus()

        self.entry.bind("<Return>", lambda e: self.submit())

        submit_btn = CTkButton(main_frame,
                               text="Continue to Calibration",
                               command=self.submit,
                               width=250,
                               height=45,
                               font=("Arial", 14, "bold"),
                               corner_radius=10)
        submit_btn.pack(pady=30)

        self.status_label = CTkLabel(main_frame,
                                     text="",
                                     text_color="#ff4444" if USE_CUSTOM_TK else "red",
                                     font=("Arial", 12))
        self.status_label.pack()

        footer = CTkLabel(main_frame,
                          text="Please ensure all sensors are connected",
                          font=("Arial", 10),
                          text_color="gray")
        footer.pack(side="bottom", pady=(0, 20))

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def submit(self):
        participant_id = self.entry.get().strip()
        if not participant_id:
            self.status_label.configure(text="⚠️ Please enter a participant ID")
            return

        self.participant_id = participant_id
        try:
            for after_id in self.tk.call('after', 'info'):
                try:
                    self.after_cancel(after_id)
                except:
                    pass
        except:
            pass
        self.destroy()

    def on_cancel(self):
        self.participant_id = None
        try:
            for after_id in self.tk.call('after', 'info'):
                try:
                    self.after_cancel(after_id)
                except:
                    pass
        except:
            pass
        self.destroy()


# ============================================================
# === Calibration Screen =====================================
# ============================================================

class CalibrationScreen(CTk):
    def __init__(self, channels, participant_id):
        super().__init__()
        print(f"🔧 Initializing CalibrationScreen...")
        self.title("Sensor Calibration")
        self.geometry("800x600")
        self.channels = channels
        self.participant_id = participant_id
        self.calibration = None
        self.calibrating = False
        self.is_destroyed = False
        self.simulation_mode = len(channels) == 0

        self.resizable(False, False)

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400)
        y = (self.winfo_screenheight() // 2) - (300)
        self.geometry(f'800x600+{x}+{y}')

        self.lift()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

        print(f"✅ CalibrationScreen window created and positioned")
        if self.simulation_mode:
            print("⚠️ CalibrationScreen running in SIMULATION mode")

        main_frame = CTkFrame(self, corner_radius=15)
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        header = CTkLabel(main_frame,
                          text="⚙️ Sensor Calibration" + (" [SIMULATION]" if self.simulation_mode else ""),
                          font=("Arial", 32, "bold"))
        header.pack(pady=(30, 10))

        info_label = CTkLabel(main_frame,
                              text=f"Participant: {participant_id}",
                              font=("Arial", 18))
        info_label.pack(pady=(0, 20))

        if self.simulation_mode:
            instructions = CTkLabel(main_frame,
                                    text="⚠️ SIMULATION MODE ACTIVE ⚠️\n"
                                         "No hardware detected - using simulated data\n"
                                         "Click 'Continue' to proceed with testing",
                                    font=("Arial", 16),
                                    justify="center",
                                    text_color="orange" if USE_CUSTOM_TK else "black")
        else:
            instructions = CTkLabel(main_frame,
                                    text="Please ensure all sensors are unloaded\n"
                                         "and in their zero position before calibrating.",
                                    font=("Arial", 16),
                                    justify="center")
        instructions.pack(pady=20)

        if self.simulation_mode:
            channel_info = CTkLabel(main_frame,
                                    text="Simulated channels: [0, 1, 2] (A, B, C)",
                                    font=("Arial", 14))
        else:
            try:
                channel_list = [vi.getChannel() for vi in channels]
                channel_info = CTkLabel(main_frame,
                                        text=f"Connected channels: {channel_list}",
                                        font=("Arial", 14))
            except Exception as e:
                print(f"⚠️ Error getting channel list: {e}")
                channel_info = CTkLabel(main_frame,
                                        text=f"Connected channels: {len(channels)}",
                                        font=("Arial", 14))
        channel_info.pack(pady=10)

        self.status_label = CTkLabel(main_frame,
                                     text="Ready to calibrate",
                                     font=("Arial", 18, "bold"))
        self.status_label.pack(pady=20)

        self.progress_label = CTkLabel(main_frame,
                                       text="",
                                       font=("Arial", 16))
        self.progress_label.pack(pady=10)

        btn_frame = CTkFrame(main_frame)
        btn_frame.pack(pady=30)

        if self.simulation_mode:
            self.btn_calibrate = CTkButton(btn_frame,
                                           text="Continue to Experiment",
                                           command=self.skip_calibration,
                                           width=300,
                                           height=60,
                                           font=("Arial", 16, "bold"),
                                           corner_radius=10)
            self.btn_calibrate.pack(padx=10)
        else:
            self.btn_calibrate = CTkButton(btn_frame,
                                           text="Start Calibration",
                                           command=self.start_calibration,
                                           width=220,
                                           height=60,
                                           font=("Arial", 16, "bold"),
                                           corner_radius=10)
            self.btn_calibrate.pack(side="left", padx=10)

            self.btn_skip = CTkButton(btn_frame,
                                      text="Skip (Use Previous)",
                                      command=self.skip_calibration,
                                      width=220,
                                      height=60,
                                      font=("Arial", 16),
                                      corner_radius=10)
            self.btn_skip.pack(side="left", padx=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        print(f"✅ CalibrationScreen GUI fully built and ready")

    def start_calibration(self):
        if self.calibrating:
            return

        self.calibrating = True
        self.btn_calibrate.configure(state="disabled")
        if hasattr(self, 'btn_skip'):
            self.btn_skip.configure(state="disabled")
        self.status_label.configure(text="🔄 Calibrating sensors...")
        self.progress_label.configure(text="Please wait, do not move sensors")

        threading.Thread(target=self.run_calibration, daemon=True).start()

    def run_calibration(self):
        duration = CONFIG['calibration_duration']
        print(f"\n🧭 Starting calibration ({duration}s)... Please ensure sensors are unloaded.\n")

        time.sleep(1.0)

        readings = {}
        try:
            for vi in self.channels:
                readings[vi.getChannel()] = []
        except Exception as e:
            print(f"⚠️ Error initializing readings: {e}")
            self.after(0, lambda: self.show_calibration_error("Failed to initialize channels"))
            return

        start = time.time()

        while time.time() - start < duration:
            if self.is_destroyed:
                return

            elapsed = time.time() - start
            remaining = duration - elapsed
            try:
                self.after(0, lambda r=remaining: self.update_progress(r))
            except:
                return

            for vi in self.channels:
                ch = vi.getChannel()
                try:
                    val = vi.getVoltageRatio()
                    readings[ch].append(val)
                except PhidgetException as e:
                    print(f"⚠️ Error reading channel {ch}: {e}")
                except Exception as e:
                    print(f"⚠️ Unexpected error reading channel {ch}: {e}")

            time.sleep(CONFIG['sampling_interval'])

        if self.is_destroyed:
            return

        # Calculate offsets
        offsets = {}
        for ch, vals in readings.items():
            if vals:
                offsets[ch] = sum(vals) / len(vals)
            else:
                offsets[ch] = 0.0
                print(f"⚠️ Warning: No readings for channel {ch}")

        if not offsets:
            self.after(0, lambda: self.show_calibration_error("No calibration data collected"))
            return

        # Save calibration
        save_calibration(offsets, participant_id=self.participant_id)

        self.calibration = offsets

        print("\n✅ Calibration complete:")
        for ch, offset in offsets.items():
            print(f"   CH{ch}: {offset:+.8f}")

        try:
            self.after(0, lambda: self.status_label.configure(text="✅ Calibration Complete!"))
            self.after(0, lambda: self.progress_label.configure(text="Sensors have been zeroed successfully"))
            self.after(1000, self.enable_continue)
        except:
            pass

    def show_calibration_error(self, message):
        """Show calibration error and allow retry"""
        if not self.is_destroyed:
            try:
                self.status_label.configure(text="❌ Calibration Failed")
                self.progress_label.configure(text=message)
                self.btn_calibrate.configure(state="normal", text="Retry Calibration")
                if hasattr(self, 'btn_skip'):
                    self.btn_skip.configure(state="normal")
                self.calibrating = False
            except:
                pass

    def update_progress(self, remaining):
        """Helper method to update progress label safely"""
        if not self.is_destroyed:
            try:
                self.progress_label.configure(text=f"Time remaining: {remaining:.1f}s")
            except:
                pass

    def enable_continue(self):
        if not self.is_destroyed:
            try:
                self.btn_calibrate.configure(text="Continue to Experiment",
                                             state="normal",
                                             command=self.finish)
                if hasattr(self, 'btn_skip'):
                    self.btn_skip.configure(state="disabled")
            except:
                pass

    def skip_calibration(self):
        self.calibration = load_calibration()
        if self.calibration:
            self.status_label.configure(text="✅ Loaded previous calibration")
            self.progress_label.configure(text="Using saved calibration values")
            print("✅ Using previous calibration")
        else:
            self.status_label.configure(text="⚠️ No previous calibration found")
            self.progress_label.configure(text="Using zero offsets (not recommended)")
            self.calibration = {}
        self.finish()

    def finish(self):
        self.is_destroyed = True
        try:
            for after_id in self.tk.call('after', 'info'):
                try:
                    self.after_cancel(after_id)
                except:
                    pass
        except:
            pass
        try:
            self.withdraw()
        except:
            pass
        self.quit()

    def on_close(self):
        self.is_destroyed = True
        self.calibration = None
        try:
            for after_id in self.tk.call('after', 'info'):
                try:
                    self.after_cancel(after_id)
                except:
                    pass
        except:
            pass
        try:
            self.withdraw()
        except:
            pass
        self.quit()


# ============================================================
# === GUI Application ========================================
# ============================================================

class PhidgetViscosityGUI(CTk):
    def __init__(self, participant_id, calibration, channels):
        super().__init__()
        self.title(f"PhidgetBridge — Syringe Study V3.2 (Participant: {participant_id})")
        self.geometry("1400x900")

        self.participant_id = participant_id
        self.update_id = None

        self.channels = channels
        self.simulation_mode = len(self.channels) == 0

        if self.simulation_mode:
            print("⚠️ Program running in SIMULATION mode")
            self.available_channels = list(range(CONFIG['num_channels']))
            self.channel_objects = {}
        else:
            self.channel_objects = {vi.getChannel(): vi for vi in self.channels}
            self.available_channels = sorted(self.channel_objects.keys())
            print(f"✅ Main GUI using {len(self.channels)} connected channel(s)")

        self.calibration = calibration
        self.trial_active = False
        self.data = {ch: [] for ch in self.available_channels}
        self.current_trial_data = []

        viscosity_labels = CONFIG['viscosity_labels']
        self.viscosity_to_channel = {label: i for i, label in enumerate(viscosity_labels)}
        self.channel_to_viscosity = {i: label for i, label in enumerate(viscosity_labels)}

        self.viscosity_trial_counts = {label: 0 for label in viscosity_labels}
        self.all_viscosities = get_counterbalanced_order(self.participant_id, viscosity_labels)
        print(f"✅ Counterbalanced order for participant {self.participant_id}: {self.all_viscosities}")

        self.current_viscosity_index = 0
        self.current_viscosity = self.all_viscosities[0]
        self.current_channel = self.viscosity_to_channel[self.current_viscosity]

        self.trial_index = 1
        self.trials_per_viscosity = CONFIG['trials_per_viscosity']
        self.experiment_complete = False

        self.trial_start_time = None
        self.data_saved = False

        self.trial_paused = False
        self.pause_start_time = None
        self.total_pause_duration = 0

        # Background auto-save setup
        self.save_queue = queue.Queue()
        self.background_save_thread = None
        self.main_data_file = os.path.join(OUTPUT_DIR, f"viscosity_data_{self.participant_id}.csv")
        self.file_initialized = False
        self.save_lock = threading.Lock()
        self.start_background_saver()

        self.build_gui()

        if self.simulation_mode:
            self.title(f"SYRINGE STUDY [SIMULATION MODE] (Participant: {participant_id})")

        self.update_plot()

    def start_background_saver(self):
        """Start the background save thread"""
        self.background_save_thread = threading.Thread(target=self._background_save_worker, daemon=True)
        self.background_save_thread.start()
        print("✅ Background auto-save thread started")
        print(f"📁 Main data file: {self.main_data_file}")

    def _background_save_worker(self):
        """Background thread that handles automatic saving after each trial"""
        while True:
            try:
                # Wait for save request from queue
                save_request = self.save_queue.get()

                if save_request == "STOP":
                    break

                trial_num = save_request

                print(f"💾 Auto-saving trial {trial_num} data in background...")

                # Perform the save
                success = self._append_trial_to_file(trial_num)

                if success:
                    print(f"✅ Trial {trial_num} auto-saved to {os.path.basename(self.main_data_file)}")
                    # Update status on main thread
                    self.after(0, lambda t=trial_num: self._update_save_status(f"Trial {t} auto-saved"))
                else:
                    print(f"⚠️ Auto-save failed for trial {trial_num}")
                    self.after(0, lambda t=trial_num: self._update_save_status(f"Auto-save failed for trial {t}",
                                                                               error=True))

            except Exception as e:
                print(f"⚠️ Error in background save worker: {e}")
                import traceback
                traceback.print_exc()

    def _update_save_status(self, message, error=False):
        """Update status label from background thread"""
        try:
            if error:
                print(f"⚠️ {message}")
            # Don't overwrite current status if trial is active
            if not self.trial_active:
                current_count = self.viscosity_trial_counts[self.current_viscosity]
                self.lbl_status.configure(
                    text=f"Status: {message} - Viscosity {self.current_viscosity} ({current_count}/{self.trials_per_viscosity})"
                )
        except Exception as e:
            print(f"⚠️ Error updating status: {e}")

    def _initialize_data_file(self):
        """Initialize the data file with header (only called once)"""
        with self.save_lock:
            if self.file_initialized:
                return True

            try:
                def write_header(f):
                    writer = csv.writer(f)
                    # Write metadata header
                    writer.writerow(['# Participant ID:', self.participant_id])
                    writer.writerow(['# Counterbalancing Order:', ', '.join(self.all_viscosities)])
                    writer.writerow(['# Bridge Gain:', CONFIG['bridge_gain']])
                    writer.writerow(['# Sampling Frequency (Hz):', CONFIG['sampling_frequency']])
                    writer.writerow(['# Force Calibration Factor:', 1841.0, 'N/(V/V)'])
                    writer.writerow([])
                    # Write data headers
                    writer.writerow(
                        ['Trial', 'Viscosity', 'Channel', 'Gain', 'Timestamp', 'Raw_Reading', 'Calibrated_Reading',
                         'Force_N']
                    )

                success, error = safe_file_write(self.main_data_file, write_header, max_attempts=3)

                if success:
                    self.file_initialized = True
                    print(f"✅ Data file initialized: {os.path.basename(self.main_data_file)}")
                    return True
                else:
                    print(f"⚠️ Failed to initialize data file: {error}")
                    return False

            except Exception as e:
                print(f"⚠️ Exception initializing data file: {e}")
                return False

    def _append_trial_to_file(self, trial_num):
        """Append trial data to the main data file"""
        with self.save_lock:
            # Initialize file if needed
            if not self.file_initialized:
                if not self._initialize_data_file():
                    return False

            try:
                # Append mode - add trial data
                with open(self.main_data_file, 'a', newline='') as f:
                    writer = csv.writer(f)

                    # Write data for this trial only
                    for channel, data_list in self.data.items():
                        for entry in data_list:
                            # Only write entries for the specified trial
                            if entry['trial'] == trial_num:
                                force_N = entry['calibrated'] * 1841.0

                                writer.writerow([
                                    entry['trial'],
                                    entry['viscosity'],
                                    entry.get('channel', channel),
                                    entry.get('gain', CONFIG['bridge_gain']),
                                    entry['timestamp'],
                                    entry['raw'],
                                    entry['calibrated'],
                                    force_N
                                ])

                return True

            except Exception as e:
                print(f"⚠️ Exception appending trial to file: {e}")
                return False

    def build_gui(self):
        """Build the complete GUI interface"""
        main_container = CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        info_frame = CTkFrame(main_container)
        info_frame.pack(fill="x", padx=5, pady=5)

        self.lbl_participant = CTkLabel(info_frame,
                                        text=f"Participant: {self.participant_id}",
                                        font=("Arial", 14, "bold"))
        self.lbl_participant.pack(side="left", padx=10, pady=5)

        self.lbl_trial = CTkLabel(info_frame,
                                  text=f"Trial: {self.trial_index}",
                                  font=("Arial", 14))
        self.lbl_trial.pack(side="left", padx=10, pady=5)

        self.lbl_viscosity = CTkLabel(info_frame,
                                      text=f"Viscosity: {self.current_viscosity} (CH{self.current_channel}) - 0/{self.trials_per_viscosity}",
                                      font=("Arial", 14))
        self.lbl_viscosity.pack(side="left", padx=10, pady=5)

        plot_frame = CTkFrame(main_container)
        plot_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.fig = Figure(figsize=(12, 6))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Sample", fontsize=12)
        self.ax.set_ylabel("Calibrated Voltage Ratio", fontsize=12)
        self.ax.set_title("Real-time Sensor Data", fontsize=14, fontweight='bold')
        self.ax.grid(True, alpha=0.3)

        self.y_min_limit = 0
        self.y_max_limit = CONFIG['plot']['initial_scale']
        self.ax.set_ylim(self.y_min_limit, self.y_max_limit)

        self.max_value_seen = CONFIG['plot']['initial_scale']

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.current_line, = self.ax.plot([], [], 'b-', linewidth=2)

        control_frame = CTkFrame(main_container)
        control_frame.pack(fill="x", padx=5, pady=5)

        self.lbl_status = CTkLabel(control_frame,
                                   text="Status: Ready",
                                   font=("Arial", 12))
        self.lbl_status.pack(pady=5)

        button_container = CTkFrame(control_frame)
        button_container.pack(pady=10, fill="x")

        left_button_frame = CTkFrame(button_container)
        left_button_frame.pack(side="left", padx=10)

        self.btn_start = CTkButton(left_button_frame,
                                   text="Start Trial",
                                   command=self.start_trial,
                                   width=120,
                                   height=40,
                                   font=("Arial", 12, "bold"))
        self.btn_start.pack(side="left", padx=5)

        self.btn_pause = CTkButton(left_button_frame,
                                   text="Pause",
                                   command=self.toggle_pause,
                                   width=120,
                                   height=40,
                                   state="disabled",
                                   font=("Arial", 12, "bold"))
        self.btn_pause.pack(side="left", padx=5)

        right_button_frame = CTkFrame(button_container)
        right_button_frame.pack(side="right", padx=10)

        self.btn_recalibrate = CTkButton(right_button_frame,
                                         text="Recalibrate",
                                         command=self.recalibrate,
                                         width=120,
                                         height=40,
                                         font=("Arial", 12))
        self.btn_recalibrate.pack(side="left", padx=5)

        self.btn_save = CTkButton(right_button_frame,
                                  text="Save Data",
                                  command=self.save_all_data,
                                  width=120,
                                  height=40,
                                  font=("Arial", 12))
        self.btn_save.pack(side="left", padx=5)

        viscosity_frame = CTkFrame(control_frame)
        viscosity_frame.pack(pady=5, anchor="e", padx=10)

        CTkLabel(viscosity_frame, text="Select Viscosity:", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        for viscosity in CONFIG['viscosity_labels']:
            channel = self.viscosity_to_channel[viscosity]
            btn = CTkButton(viscosity_frame,
                            text=f"{viscosity} (CH{channel})",
                            command=lambda v=viscosity: self.select_viscosity(v),
                            width=80,
                            height=35,
                            font=("Arial", 12, "bold"))
            btn.pack(side="left", padx=2)

    def select_viscosity(self, viscosity):
        """Select which viscosity to test with validation"""
        if self.trial_active:
            messagebox.showwarning("Trial Active", "Please stop the current trial before changing viscosity")
            return

        try:
            self.current_viscosity = viscosity
            self.current_channel = self.viscosity_to_channel[viscosity]
            self.current_viscosity_index = self.all_viscosities.index(viscosity)

            current_count = self.viscosity_trial_counts[self.current_viscosity]
            self.lbl_viscosity.configure(
                text=f"Viscosity: {self.current_viscosity} (CH{self.current_channel}) - {current_count}/{self.trials_per_viscosity}"
            )

            self.lbl_status.configure(
                text=f"Status: Viscosity {viscosity} selected (Channel {self.current_channel}) - {current_count}/{self.trials_per_viscosity} complete"
            )
            print(f"✅ Manually selected Viscosity {viscosity} → Channel {self.current_channel}")
        except Exception as e:
            print(f"⚠️ Error selecting viscosity: {e}")
            self.lbl_status.configure(text=f"Status: Error selecting viscosity")

    def notify_condition_change(self, new_condition):
        """Show popup notification for viscosity change"""
        try:
            channel = self.viscosity_to_channel.get(new_condition, "Unknown")
            message = (f"🔄 Condition changed!\n\n"
                       f"Prepare for next viscosity: {new_condition} (CH{channel}).\n\n"
                       "Click OK when you are ready to continue.")
            print(message)
            messagebox.showinfo("Condition Change", message)
        except Exception as e:
            print(f"⚠️ Could not show condition-change popup: {e}")

    def play_beep(self, frequency, duration_ms):
        """Play a beep sound with error handling"""
        try:
            if AUDIO_METHOD == 'winsound':
                import winsound
                frequency = max(37, min(32767, frequency))
                winsound.Beep(int(frequency), int(duration_ms))
                return True
            elif AUDIO_METHOD == 'pygame':
                import pygame
                import numpy as np
                sample_rate = 22050
                duration_sec = duration_ms / 1000.0
                samples = int(sample_rate * duration_sec)

                wave = np.sin(2 * np.pi * frequency * np.linspace(0, duration_sec, samples))
                wave = (wave * 32767).astype(np.int16)

                stereo_wave = np.column_stack((wave, wave))
                sound = pygame.sndarray.make_sound(stereo_wave)
                sound.play()
                time.sleep(duration_sec)
                return True
            else:
                time.sleep(duration_ms / 1000.0)
                print('\a')
                return False
        except Exception as e:
            print(f"⚠️ Beep failed: {e}")
            time.sleep(duration_ms / 1000.0)
            return False

    def play_countdown_beeps(self):
        """Play audio countdown"""
        if not CONFIG['audio']['enabled']:
            time.sleep(CONFIG['countdown_duration'])
            return

        print("🔊 Starting countdown...")

        try:
            duration_ms = int(CONFIG['countdown_duration'] * 1000)
            frequency = CONFIG['audio']['frequency']

            self.after(0, lambda: self.lbl_status.configure(text="Status: Get ready... Recording will start!"))
            print(f"  Playing start tone ({CONFIG['countdown_duration']}s @ {frequency}Hz)...")
            self.play_beep(frequency, duration_ms)
            print("✅ Countdown complete!")

        except Exception as e:
            print(f"⚠️ Countdown error: {e}")
            time.sleep(CONFIG['countdown_duration'])

    def start_trial(self):
        """Start a new trial with countdown"""
        if self.trial_active:
            return

        self.btn_start.configure(state="disabled")
        self.btn_pause.configure(state="disabled")

        self.y_min_limit = 0
        self.y_max_limit = CONFIG['plot']['initial_scale']
        self.max_value_seen = CONFIG['plot']['initial_scale']
        self.ax.set_ylim(self.y_min_limit, self.y_max_limit)

        self.current_trial_data = []

        self.lbl_status.configure(text=f"Status: Preparing... Get ready!")

        threading.Thread(target=self._countdown_and_collect, daemon=True).start()

    def _countdown_and_collect(self):
        """Play countdown then start data collection"""
        print("\n" + "=" * 50)
        print("🎬 TRIAL STARTING - COUNTDOWN SEQUENCE")
        print("=" * 50)

        self.play_countdown_beeps()

        print("=" * 50)
        print("📊 DATA COLLECTION STARTING NOW")
        print("=" * 50 + "\n")

        self.trial_start_time = time.time()
        self.total_pause_duration = 0
        self.trial_paused = False

        self.trial_active = True

        self.after(0, lambda: self.btn_start.configure(text="Stop Trial", state="normal", command=self.stop_trial))
        self.after(0, lambda: self.btn_pause.configure(state="normal"))
        self.after(0, lambda: self.lbl_status.configure(
            text=f"Status: Recording Viscosity {self.current_viscosity} (CH{self.current_channel})..."))

        self.collect_data()

    def toggle_pause(self):
        """Toggle pause state during trial"""
        if not self.trial_active:
            return

        try:
            if self.trial_paused:
                print("▶️ Continuing data collection...")

                if self.pause_start_time:
                    pause_duration = time.time() - self.pause_start_time
                    self.total_pause_duration += pause_duration
                    print(f"   Paused for {pause_duration:.2f}s (Total pause time: {self.total_pause_duration:.2f}s)")

                self.trial_paused = False
                self.pause_start_time = None

                self.btn_pause.configure(text="Pause")
                self.lbl_status.configure(
                    text=f"Status: Recording Viscosity {self.current_viscosity} (CH{self.current_channel})..."
                )
            else:
                print("⏸️ Pausing data collection...")
                self.trial_paused = True
                self.pause_start_time = time.time()

                self.btn_pause.configure(text="Continue")
                self.lbl_status.configure(
                    text=f"Status: PAUSED - Viscosity {self.current_viscosity} (CH{self.current_channel})"
                )
        except Exception as e:
            print(f"⚠️ Error toggling pause: {e}")

    def collect_data(self):
        """Collect data from sensors with error handling"""
        import random

        while self.trial_active:
            if self.trial_paused:
                time.sleep(0.1)
                continue

            try:
                if self.simulation_mode:
                    base_values = {0: 0.5, 1: 0.3, 2: 0.7}
                    base = base_values.get(self.current_channel, 0.5)
                    raw_reading = base + random.uniform(-0.05, 0.05)
                    gain = CONFIG['bridge_gain']
                else:
                    vi = self.channel_objects.get(self.current_channel)
                    if vi is None:
                        print(f"⚠️ Channel {self.current_channel} not available")
                        time.sleep(CONFIG['sampling_interval'])
                        continue

                    try:
                        raw_reading = vi.getVoltageRatio()
                    except PhidgetException as e:
                        print(f"⚠️ Error reading channel {self.current_channel}: {e}")
                        time.sleep(CONFIG['sampling_interval'])
                        continue

                    try:
                        from Phidget22.BridgeGain import BridgeGain
                        bridge_gain_enum = vi.getBridgeGain()

                        gain_enum_to_value = {
                            BridgeGain.BRIDGE_GAIN_1: 1,
                            BridgeGain.BRIDGE_GAIN_2: 2,
                            BridgeGain.BRIDGE_GAIN_4: 4,
                            BridgeGain.BRIDGE_GAIN_8: 8,
                            BridgeGain.BRIDGE_GAIN_16: 16,
                            BridgeGain.BRIDGE_GAIN_32: 32,
                            BridgeGain.BRIDGE_GAIN_64: 64,
                            BridgeGain.BRIDGE_GAIN_128: 128
                        }
                        gain = gain_enum_to_value.get(bridge_gain_enum, CONFIG['bridge_gain'])
                    except:
                        gain = CONFIG['bridge_gain']

                offset = self.calibration.get(self.current_channel, 0.0)
                calibrated_reading = raw_reading - offset

                current_time = time.time()
                if self.trial_start_time:
                    relative_timestamp = current_time - self.trial_start_time - self.total_pause_duration
                else:
                    relative_timestamp = 0

                self.current_trial_data.append(calibrated_reading)
                self.data[self.current_channel].append({
                    'timestamp': relative_timestamp,
                    'trial': self.trial_index,
                    'viscosity': self.current_viscosity,
                    'channel': self.current_channel,
                    'gain': gain,
                    'raw': raw_reading,
                    'calibrated': calibrated_reading
                })

            except Exception as e:
                print(f"⚠️ Unexpected error in data collection: {e}")

            time.sleep(CONFIG['sampling_interval'])

    def update_plot(self):
        """Update plot with error handling"""
        try:
            if self.current_line is not None and self.current_trial_data:
                y = self.current_trial_data
                x = list(range(len(y)))
                self.current_line.set_data(x, y)

                if y:
                    max_value = max(y)

                    if max_value > self.max_value_seen:
                        self.max_value_seen = max_value
                        new_limit = max_value * CONFIG['plot']['scale_padding']
                        self.y_min_limit = 0
                        self.y_max_limit = new_limit
                        self.ax.set_ylim(self.y_min_limit, self.y_max_limit)

                self.ax.set_xlim(0, max(len(x), 10))
                self.canvas.draw_idle()
        except Exception as e:
            print(f"⚠️ Error updating plot: {e}")

        self.update_id = self.after(300, self.update_plot)

    def stop_trial(self):
        """Stop current trial with error handling"""
        if not self.trial_active:
            return

        try:
            self.trial_active = False
            self.trial_paused = False

            self.btn_start.configure(text="Start Trial", state="normal", command=self.start_trial)
            self.btn_pause.configure(text="Pause", state="disabled")

            self.viscosity_trial_counts[self.current_viscosity] += 1

            current_count = self.viscosity_trial_counts[self.current_viscosity]

            self.lbl_viscosity.configure(
                text=f"Viscosity: {self.current_viscosity} (CH{self.current_channel}) - {current_count}/{self.trials_per_viscosity}"
            )

            self.lbl_status.configure(
                text=f"Status: Trial stopped. Viscosity {self.current_viscosity}: {current_count}/{self.trials_per_viscosity} complete"
            )

            # *** NEW: Queue background save after trial completion ***
            self.save_queue.put(self.trial_index)
            print(f"📋 Queued auto-save for trial {self.trial_index}")

            self.after(500, self.next_trial)
        except Exception as e:
            print(f"⚠️ Error stopping trial: {e}")

    def next_trial(self):
        """Advance to next trial with error handling"""
        try:
            moved_to_new_viscosity = False
            if self.viscosity_trial_counts[self.current_viscosity] >= self.trials_per_viscosity:
                prev_viscosity = self.current_viscosity
                self.current_viscosity_index += 1

                if self.current_viscosity_index >= len(self.all_viscosities):
                    self.experiment_complete = True
                    self.show_experiment_complete_dialog()
                    return

                self.current_viscosity = self.all_viscosities[self.current_viscosity_index]
                self.current_channel = self.viscosity_to_channel[self.current_viscosity]
                moved_to_new_viscosity = True

                print(f"\n✅ Viscosity {prev_viscosity} COMPLETE!")
                print(f"🔄 Switching to Viscosity {self.current_viscosity} (Channel {self.current_channel})\n")

            self.trial_index += 1
            self.lbl_trial.configure(text=f"Trial: {self.trial_index}")

            if moved_to_new_viscosity:
                self.notify_condition_change(self.current_viscosity)

            self.current_trial_data = []
            try:
                self.current_line.set_data([], [])
            except Exception:
                pass

            self.y_min_limit = 0
            self.y_max_limit = CONFIG['plot']['initial_scale']
            self.max_value_seen = CONFIG['plot']['initial_scale']
            self.ax.set_ylim(self.y_min_limit, self.y_max_limit)
            self.ax.set_xlim(0, 10)

            try:
                self.canvas.draw()
            except Exception:
                pass

            current_count = self.viscosity_trial_counts[self.current_viscosity]
            self.lbl_viscosity.configure(
                text=f"Viscosity: {self.current_viscosity} (CH{self.current_channel}) - {current_count}/{self.trials_per_viscosity}"
            )

            self.lbl_status.configure(
                text=f"Status: Ready - Viscosity {self.current_viscosity} ({current_count}/{self.trials_per_viscosity}). Press Start Trial."
            )
        except Exception as e:
            print(f"⚠️ Error in next_trial: {e}")

    def show_experiment_complete_dialog(self):
        """Show dialog when experiment complete"""
        try:
            print("\n" + "=" * 60)
            print("🎉 DATA COLLECTION COMPLETE!")
            print("=" * 60)
            print(f"Total trials completed: {self.trial_index}")
            for viscosity in self.all_viscosities:
                count = self.viscosity_trial_counts[viscosity]
                print(f"  {viscosity}: {count} trials")
            print("=" * 60 + "\n")

            result = messagebox.askyesno(
                "Experiment Complete",
                f"🎉 All trials completed!\n\n"
                f"Total trials: {self.trial_index}\n"
                f"{''.join([f'{v}: {self.viscosity_trial_counts[v]} trials' + chr(10) for v in self.all_viscosities])}\n"
                f"Would you like to continue with more trials?\n\n"
                f"Select 'Yes' to continue or 'No' to end the experiment.",
                icon='info'
            )

            if result:
                print("✅ Continuing experiment...")
                self.experiment_complete = False
                self.lbl_status.configure(text="Status: Experiment continuing - Select viscosity and press Start")
            else:
                print("✅ Ending experiment...")
                self.lbl_status.configure(text="Status: Experiment ended - You may close the window")

                save_result = messagebox.askyesno(
                    "Save Data Now",
                    "Would you like to create a manual backup of all data?\n\n"
                    "(Data has been auto-saved after each trial)\n\n"
                    "This creates a timestamped copy for safety.",
                    icon='question'
                )

                if save_result:
                    self.save_all_data()

                self.after(1000, self.on_close)
        except Exception as e:
            print(f"⚠️ Error showing completion dialog: {e}")

    def save_all_data(self):
        """Save all data to a timestamped backup file with comprehensive error handling"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(OUTPUT_DIR, f"viscosity_data_{self.participant_id}_{timestamp}_backup.csv")

        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                def write_data(f):
                    writer = csv.writer(f)

                    # Write metadata header
                    writer.writerow(['# Participant ID:', self.participant_id])
                    writer.writerow(['# Counterbalancing Order:', ', '.join(self.all_viscosities)])
                    writer.writerow(['# Bridge Gain:', CONFIG['bridge_gain']])
                    writer.writerow(['# Sampling Frequency (Hz):', CONFIG['sampling_frequency']])
                    writer.writerow(['# Force Calibration Factor:', 1841.0, 'N/(V/V)'])
                    writer.writerow([])

                    # Write data headers
                    writer.writerow(
                        ['Trial', 'Viscosity', 'Channel', 'Gain', 'Timestamp', 'Raw_Reading', 'Calibrated_Reading',
                         'Force_N'])

                    for channel, data_list in self.data.items():
                        for entry in data_list:
                            force_N = entry['calibrated'] * 1841.0

                            writer.writerow([
                                entry['trial'],
                                entry['viscosity'],
                                entry.get('channel', channel),
                                entry.get('gain', CONFIG['bridge_gain']),
                                entry['timestamp'],
                                entry['raw'],
                                entry['calibrated'],
                                force_N
                            ])

                success, error = safe_file_write(filename, write_data, max_attempts=1)

                if success:
                    self.data_saved = True
                    messagebox.showinfo("Backup Created", f"Backup saved to:\n{os.path.basename(filename)}")
                    self.lbl_status.configure(text=f"Status: Backup saved to {os.path.basename(filename)}")
                    print(f"💾 Backup saved to {filename}")
                    return
                else:
                    # File locked or permission error
                    if attempt < max_attempts - 1:
                        result = messagebox.askretrycancel(
                            "File Access Error",
                            f"Cannot save to '{os.path.basename(filename)}'.\n\n"
                            f"Error: {error}\n\n"
                            f"The file may be open in another program (Excel, text editor, etc.).\n\n"
                            f"Please close the file and click 'Retry'.\n\n"
                            f"Attempt {attempt + 1} of {max_attempts}",
                            icon='warning'
                        )
                        if not result:
                            # User cancelled
                            print("⚠️ User cancelled save operation")
                            return
                        time.sleep(0.5)
                    else:
                        # Final attempt - try alternative filename
                        alt_filename = os.path.join(OUTPUT_DIR,
                                                    f"viscosity_data_{self.participant_id}_{timestamp}_backup2.csv")
                        messagebox.showwarning(
                            "Save Failed",
                            f"Could not save to '{os.path.basename(filename)}'.\n\n"
                            f"Trying alternative filename:\n'{os.path.basename(alt_filename)}'"
                        )
                        filename = alt_filename

            except Exception as e:
                print(f"⚠️ Unexpected error saving data (attempt {attempt + 1}): {e}")
                if attempt >= max_attempts - 1:
                    messagebox.showerror(
                        "Save Failed",
                        f"Failed to save backup after {max_attempts} attempts.\n\n"
                        f"Error: {e}\n\n"
                        f"Your main data file should still be intact:\n{os.path.basename(self.main_data_file)}"
                    )
                    return

        # If we get here, all attempts failed
        messagebox.showerror(
            "Save Failed",
            f"Could not save backup after {max_attempts} attempts.\n\n"
            f"Your main data file should still be intact:\n{os.path.basename(self.main_data_file)}"
        )

    def recalibrate(self):
        """Recalibrate sensors with error handling"""
        if self.trial_active:
            messagebox.showwarning("Trial Active", "Please stop the current trial before recalibrating.")
            return

        try:
            if self.update_id:
                self.after_cancel(self.update_id)
                self.update_id = None

            self.withdraw()

            cal_window = CalibrationScreen(self.channels, self.participant_id)
            cal_window.mainloop()

            new_calibration = cal_window.calibration

            try:
                cal_window.destroy()
            except:
                pass

            self.deiconify()

            if new_calibration is not None:
                self.calibration = new_calibration
                self.lbl_status.configure(text="Status: Recalibration complete")
                print("✅ Recalibration complete, new values loaded")
            else:
                self.lbl_status.configure(text="Status: Recalibration cancelled")
                print("⚠️ Recalibration cancelled")

            self.update_plot()

        except Exception as e:
            print(f"⚠️ Error during recalibration: {e}")
            self.lbl_status.configure(text="Status: Recalibration error")
            try:
                self.deiconify()
            except:
                pass
            if self.update_id is None:
                self.update_plot()

    def on_close(self):
        """Clean up on close with comprehensive error handling"""
        self.trial_active = False

        # Stop background save thread
        try:
            self.save_queue.put("STOP")
            if self.background_save_thread and self.background_save_thread.is_alive():
                self.background_save_thread.join(timeout=2.0)
                print("✅ Background save thread stopped")
        except Exception as e:
            print(f"⚠️ Error stopping background save thread: {e}")

        try:
            if self.update_id:
                self.after_cancel(self.update_id)
        except:
            pass

        has_data = any(len(data_list) > 0 for data_list in self.data.values())

        if has_data:
            print("\n" + "=" * 60)
            print("ℹ️ Data has been automatically saved after each trial")
            print(f"📁 Main data file: {os.path.basename(self.main_data_file)}")
            print("=" * 60 + "\n")
        else:
            print("ℹ️ No data to save")

        # Close Phidget channels
        for vi in self.channels:
            try:
                vi.close()
            except Exception as e:
                print(f"⚠️ Error closing channel: {e}")

        try:
            self.destroy()
        except Exception as e:
            print(f"⚠️ Error destroying window: {e}")


# ============================================================
# === Main ===================================================
# ============================================================

if __name__ == "__main__":
    channels = []
    try:
        print("Step 1: Showing participant dialog...")
        dialog = ParticipantDialog()
        dialog.mainloop()

        if not dialog.participant_id:
            print("Experiment cancelled - no participant ID entered")
            exit()

        participant_id = dialog.participant_id
        print(f"✅ Participant ID: {participant_id}")

        print("Step 2: Connecting to Phidget channels...")
        channels = connect_channels()
        if not channels:
            print("⚠️ No Phidget channels detected.")
            root = tk.Tk()
            root.withdraw()
            result = messagebox.askyesno(
                "No Phidgets Detected",
                "No Phidget channels were detected.\n\n"
                "Would you like to continue in SIMULATION mode?\n"
                "(Random data will be generated for testing)",
                icon='warning'
            )
            root.destroy()

            if not result:
                print("Experiment cancelled - no Phidgets and user declined simulation")
                exit()

            print("⚠️ Running in SIMULATION MODE with mock data")
            channels = []

        if channels:
            print(f"✅ Connected to {len(channels)} channels")
        else:
            print("⚠️ Running in simulation mode (no hardware)")

        print("Step 3: Showing calibration screen...")
        cal_screen = CalibrationScreen(channels, participant_id)
        cal_screen.mainloop()

        calibration = cal_screen.calibration

        try:
            if cal_screen.winfo_exists():
                cal_screen.withdraw()
                cal_screen.update()
                cal_screen.destroy()
                print("✅ Calibration window closed")
        except Exception as e:
            print(f"Note: Calibration window cleanup ({e})")

        if calibration is None:
            print("Experiment cancelled - no calibration performed")
            for vi in channels:
                try:
                    vi.close()
                except:
                    pass
            exit()

        print(f"✅ Calibration complete: {calibration}")

        print("Step 4: Starting main application...")
        app = PhidgetViscosityGUI(participant_id, calibration, channels)
        app.protocol("WM_DELETE_WINDOW", app.on_close)
        print("✅ Application started successfully")
        app.mainloop()

    except KeyboardInterrupt:
        print("\n⚠️ Program interrupted by user")
    except Exception as e:
        print(f"⚠️ Fatal error: {e}")
        import traceback

        traceback.print_exc()

        # Try to show error dialog
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Fatal Error",
                f"A fatal error occurred:\n\n{e}\n\n"
                f"Please check the console for details."
            )
            root.destroy()
        except:
            pass

    finally:
        print("Cleaning up...")
        try:
            if 'channels' in locals():
                for vi in channels:
                    try:
                        vi.close()
                    except:
                        pass
        except:
            pass
        print("✅ Cleanup complete")