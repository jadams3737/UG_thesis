import numpy as np

def steady_state_error(exp_data, sim_data, min_stable_period=20):
    initial_value_range = 0.05
    movement_threshold = 1  # degrees of deviation
    steady_threshold = 1    # degrees of deviation

    # Initial value is the mean of the initial data
    initial_value = np.mean(exp_data[:int(len(exp_data) * initial_value_range)])

    # Find where the data starts to deviate from the initial value, indicating movement
    move_start = np.argmax(np.abs(exp_data - initial_value) > movement_threshold)

    # Find the last point oustide the movement thrshold
    move_end = len(exp_data) - np.argmax(np.abs(exp_data[::-1] - initial_value) > movement_threshold)

    # If move_end couldn't be determined, default to using the end of the data
    if move_end == move_start:
        move_end = len(exp_data) - 1
    
    # Estimate the target value from the middle 20 percent of the move region
    move_region = exp_data[move_start:move_end]
    target_value = np.mean(move_region[int(len(move_region) * 0.4):int(len(move_region) * 0.6)])

    # Identify data within a threshold of the target value
    within_threshold = np.abs(move_region - target_value) < (steady_threshold)
    steady_start = None

    # Find the first sequence of at least `min_stable_period` points within the threshold
    for i in range(len(within_threshold) - min_stable_period):
        if np.all(within_threshold[i:i + min_stable_period]):
            steady_start = i + move_start
            break

    # If steady_start couldn't be determined, default to using the start of the move region
    if steady_start is None:
        print("Warning: No steady-state region found. Defaulting to using the midpoint of the move region.")
        steady_start = move_start

    # Find the last sequence of `mid_stable_period` points within the threshold
    steady_end = None
    for i in range(len(within_threshold) - min_stable_period, 0, -1):
        if np.all(within_threshold[i:i + min_stable_period]):
            steady_end = i + move_start + min_stable_period
            break
    
    # If steady_end couldn't be determined, default to using the end of the target region
    if steady_end is None:
        print("Warning: No steady-state region found. Defaulting to using the end of the move region.")
        steady_end = move_end

    # If no movement detected, there is no steady-state region
    if np.max(np.abs(exp_data - initial_value)) < 1:    # 1 degree of deviation
        steady_start = None
        steady_end = None
        print("Warning: No movement detected. Setting the whole region as steady-state.")

    # Print the initial value
    print(f"Initial value: {initial_value:.2f}")

    # Calculate the error if a steady-state region was found
    if steady_start is None:
        error_percent = None
        error_abs = None
        move_start = None
        oscillation_amplitude = None
    else:
        # Calculate steady-state averages for experimental and simulation data
        exp_steady_state = np.mean(exp_data[steady_start:steady_end])
        sim_steady_state = np.mean(sim_data[steady_start:steady_end])

        # Calculate the percentage error
        exp_steady_relative = abs(exp_steady_state - initial_value)
        sim_steady_relative = abs(sim_steady_state - initial_value)
        error_percent = 100 * abs((sim_steady_relative - exp_steady_relative) / exp_steady_relative)
        error_abs = abs(exp_steady_state - sim_steady_state)

        print(f"Exp steady-state: {exp_steady_state:.2f}")
        print(f"Sim steady-state: {sim_steady_state:.2f}")

        # Identify the amplitude of oscillation in the steady-state region
        oscillation_amplitude = np.max(exp_data[steady_start:steady_end]) - np.min(exp_data[steady_start:steady_end])


    return error_percent, error_abs, steady_start, steady_end, move_start, oscillation_amplitude
