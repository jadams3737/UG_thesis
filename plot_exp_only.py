import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from steady_state_error import steady_state_error


# -------------- Modify  as needed --------------
SAVE_SEPERATELY = False  # Toggle to save plots separately or as one image
# ----------------------------------------------

# Load the experimental and simulation data
# exp_data = pd.read_csv(f'exp_results/pool_control_both.csv')
exp_data = pd.read_csv(f'exp_results/pool_f_position3.csv')

# Extract experimental data
exp_timestamps = exp_data['Timestamp'].values
exp_pitches = exp_data['Pitch'].values
exp_rolls = exp_data['Roll'].values

# Find average of first 30 exp pitch and roll values
exp_pitch_start = np.mean(exp_pitches[:30])
exp_roll_start = np.mean(exp_rolls[:30])

# Convert experimental timestamps to relative time starting from zero
exp_timestamps_relative = exp_timestamps - exp_timestamps[0]

# Construct a new DataFrame for aligned data
aligned_data = pd.DataFrame({
    'Exp_Timestamp': exp_timestamps_relative,
    'Exp_Pitch': exp_pitches,
    'Exp_Roll': exp_rolls
})

if not SAVE_SEPERATELY:
    plt.figure(figsize=(10, 7))

# Plot experimental and simulated pitch data
if SAVE_SEPERATELY:
    plt.figure("pitch_plot", figsize=(10, 3.5))
else:
    plt.subplot(2, 1, 1)      # Plot as a subplot
plt.plot(aligned_data['Exp_Timestamp'], aligned_data['Exp_Pitch'], label='Experimental', color='blue')
if not SAVE_SEPERATELY:
    plt.title('ROV Pitch Data')
plt.xlabel('Time, seconds')
plt.ylabel('Pitch, degrees')
plt.legend()
plt.grid()
plt.tight_layout()


# Plot experimental and simulated roll data
if SAVE_SEPERATELY: 
    plt.figure("roll_plot", figsize=(10, 3.5))
else:
    plt.subplot(2, 1, 2)  # Plot as a subplot
plt.plot(aligned_data['Exp_Timestamp'], aligned_data['Exp_Roll'], label='Experimental', color='blue')

if not SAVE_SEPERATELY:
    plt.title('ROV Roll Data')
plt.xlabel('Time, seconds')
plt.ylabel('Roll, degrees')
plt.legend()
plt.grid()
plt.tight_layout()

plt.show()



