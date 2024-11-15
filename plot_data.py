import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from steady_state_error import steady_state_error


# -------------- Modify  as needed --------------
position = 'bl'
SAVE_SEPERATELY = True  # Toggle to save plots separately or as one image
# ----------------------------------------------

# Load the experimental and simulation data
exp_data = pd.read_csv(f'exp_results/pool_{position}_position3.csv')
sim_data = pd.read_csv(f'sim_results/from_zero/sim_{position}_position.csv')

# Extract experimental data
exp_timestamps = exp_data['Timestamp'].values
exp_pitches = exp_data['Pitch'].values
exp_rolls = exp_data['Roll'].values

# Extract simulation data
sim_timestamps = sim_data['Timestamp'].values
sim_pitches = sim_data['Pitch'].values
sim_rolls = sim_data['Roll'].values

# Find average of first 30 exp pitch and roll values
exp_pitch_start = np.mean(exp_pitches[:30])
exp_roll_start = np.mean(exp_rolls[:30])

# Convert experimental timestamps to relative time starting from zero
exp_timestamps_relative = exp_timestamps - exp_timestamps[0]

# Interpolate simulation data to align with experimental timestamps
sim_pitches_interpolated = np.interp(exp_timestamps_relative, sim_timestamps, sim_pitches)
sim_rolls_interpolated = np.interp(exp_timestamps_relative, sim_timestamps, sim_rolls)

# Additional dataset for shifted simulation data
sim_pitches_shifted = sim_pitches_interpolated + (exp_pitch_start - sim_pitches_interpolated[0])
sim_rolls_shifted = sim_rolls_interpolated + (exp_roll_start - sim_rolls_interpolated[0])


# Construct a new DataFrame for aligned data
aligned_data = pd.DataFrame({
    'Exp_Timestamp': exp_timestamps_relative,
    'Exp_Pitch': exp_pitches,
    'Exp_Roll': exp_rolls,
    'Sim_Pitch': sim_pitches_interpolated,
    'Sim_Roll': sim_rolls_interpolated,
    'Shifted_Sim_Pitch': sim_pitches_shifted,
    'Shifted_Sim_Roll': sim_rolls_shifted
})

# Calculate the steady-state region and error
pitch_error_percent, pitch_error_abs, pitch_steady_start, pitch_steady_end, pitch_move_start, pitch_ss_amplitude = steady_state_error(exp_pitches, sim_pitches_shifted)
roll_error_percent, roll_error_abs, roll_steady_start, roll_steady_end, roll_move_start, roll_ss_amplitude = steady_state_error(exp_rolls, sim_rolls_shifted)

if not SAVE_SEPERATELY:
    plt.figure(figsize=(10, 7))

# Plot experimental and simulated pitch data
if SAVE_SEPERATELY:
    plt.figure(f"{position}_pitch_plot", figsize=(10, 3.5))
else:
    plt.subplot(2, 1, 1)      # Plot as a subplot
plt.plot(aligned_data['Exp_Timestamp'], aligned_data['Exp_Pitch'], label='Experimental', color='blue')
# plt.plot(aligned_data['Exp_Timestamp'], aligned_data['Sim_Pitch'], label='Simulation', color='red', linestyle=':')
plt.plot(aligned_data['Exp_Timestamp'], aligned_data['Shifted_Sim_Pitch'], label='Simulation (shifted)', color='red')
if pitch_steady_start is not None:
    plt.scatter(aligned_data['Exp_Timestamp'][pitch_steady_start:pitch_steady_end], 
                aligned_data['Exp_Pitch'][pitch_steady_start:pitch_steady_end], 
                color='green', s=3, label='Steady-State Region (Exp)', zorder=3)
    plt.scatter(aligned_data['Exp_Timestamp'][pitch_steady_start:pitch_steady_end],
                aligned_data['Shifted_Sim_Pitch'][pitch_steady_start:pitch_steady_end], color='purple', s=3, label='Steady-State Region (Sim)', zorder=3)
if not SAVE_SEPERATELY:
    plt.title('ROV Pitch Data')
plt.xlabel('Time, seconds')
plt.ylabel('Pitch, degrees')
plt.legend()
plt.grid()
plt.tight_layout()

if SAVE_SEPERATELY:
    plt.savefig(f'final_figures/pitch_plot_{position}_position.png')

# Plot experimental and simulated roll data
if SAVE_SEPERATELY: 
    plt.figure(f"{position}_roll_plot", figsize=(10, 3.5))
else:
    plt.subplot(2, 1, 2)  # Plot as a subplot
plt.plot(aligned_data['Exp_Timestamp'], aligned_data['Exp_Roll'], label='Experimental', color='blue')
# plt.plot(aligned_data['Exp_Timestamp'], aligned_data['Sim_Roll'], label='Simulation', color='red', linestyle=':')
plt.plot(aligned_data['Exp_Timestamp'], aligned_data['Shifted_Sim_Roll'], label='Simulation (shifted)', color='red')
if roll_steady_start is not None:
    plt.scatter(aligned_data['Exp_Timestamp'][roll_steady_start:roll_steady_end],
                aligned_data['Exp_Roll'][roll_steady_start:roll_steady_end],
                color='green', s=3, label='Steady-State Region (Exp)', zorder=3)
    plt.scatter(aligned_data['Exp_Timestamp'][roll_steady_start:roll_steady_end],
                aligned_data['Shifted_Sim_Roll'][roll_steady_start:roll_steady_end], color='purple', s=3, label='Steady-State Region (Sim)', zorder=3)
if not SAVE_SEPERATELY:
    plt.title('ROV Roll Data')
plt.xlabel('Time, seconds')
plt.ylabel('Roll, degrees')
plt.legend()
plt.grid()
plt.tight_layout()

if SAVE_SEPERATELY:
    plt.savefig(f'final_figures/roll_plot_{position}_position.png')
    print(f'Plots saved as pitch_plot_{position}_position.png and roll_plot_{position}_position.png')
else:
    plt.savefig(f'final_figures/plot_{position}_position.png')  # Save both plots as one image
    print(f'Plot saved as plot_{position}_position.png')

# Pitch Statistics
if pitch_error_percent is None:
    print("Warning: No steady-state region found for pitch data.")
else:
    print('-------- Pitch Statistics --------')
    print(f'Pitch Error Percentage: {pitch_error_percent:.2f}%')
    print(f'Pitch Error Absolute: {pitch_error_abs:.2f} degrees')
    print(f'Pitch Amplitude of Oscillation: {pitch_ss_amplitude:.2f} degrees')

    # Calculate the experimental response time for pitch
    response_time = exp_timestamps_relative[pitch_steady_start] - exp_timestamps_relative[pitch_move_start]
    print(f'Experimental Response Time: {response_time:.2f} seconds')
    
# Roll Statistics
if roll_error_percent is None:
    print("Warning: No steady-state region found for roll data.")
else:
    print('-------- ROll Statistics --------')
    print(f'Roll Error Percentage: {roll_error_percent:.2f}%')
    print(f'Roll Error Absolute: {roll_error_abs:.2f} degrees')
    print(f'Roll Amplitude of Oscillation: {roll_ss_amplitude:.2f} degrees')

    # Calculate the experimental response time for roll
    response_time = exp_timestamps_relative[roll_steady_start] - exp_timestamps_relative[roll_move_start]
    print(f'Experimental Response Time: {response_time:.2f} seconds')



plt.show()



