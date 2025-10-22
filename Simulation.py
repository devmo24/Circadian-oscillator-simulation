import math, random

# Initial values (buffer is used for step calculations)
A = 1000
A_active_percent = 1
B = 350
B_production_rate = 15
A_active_percent_buffer = A_active_percent
B_buffer = B
B_production_rate_buffer = B_production_rate
bacteria = 0
previous_bacteria = bacteria
delta_bacteria = 0
bacteria_add_time = 600
bacteria_to_add = 300
exposure = "stimulation"
simulate_desync = False
desync_factor = 10 # percent
desync_sampling = 500

# Kinetic rates
maximum_production_rate = 100
production_efficiency = 5
production_change_rate = 0.5 # percent
degradation_rate = 4.96 # percent
repression_efficiency = 3
repression_rate = 2.8 # percent

steps = 2000
current_step = 0
save_step_interval = 10

# Create list to store the state of the step
# Not useful if not simulating desync
if simulate_desync:
    A_active_percent_samples = [A_active_percent] * desync_sampling
    B_samples = [B] * desync_sampling
    B_production_rate_samples = [B_production_rate] * desync_sampling

with open("Circadian simulation.csv", "w") as file:
    file.write("Time,"
               "Active A (%),"
               "B\n")

    # Run simulation once if not simulating desync, else run sampling, as determined by the desync sampling variable
    if simulate_desync:
        sampling = desync_sampling
    else:
        sampling = 1

    while current_step < steps:

        # Determine amount of bacteria

        # add bacteria once
        if exposure == "stimulation":
            if current_step == bacteria_add_time:
                bacteria = bacteria_to_add

        # bacterial exposure oscillates
        elif exposure == "oscillation":
            if current_step >= bacteria_add_time:
                bacteria = 30 + 25 * math.cos(((current_step / 10) - 62) * 2 * math.pi / 24)

        delta_bacteria = bacteria - previous_bacteria

        # Simulate all the samples
        for i in range(sampling):

            # set variables of the current sample
            if simulate_desync:
                A_active_percent_current = A_active_percent_samples[i]
                B_current = B_samples[i]
                B_production_rate_current = B_production_rate_samples[i]
                A_active_percent_buffer = A_active_percent_current
                B_buffer = B_current
                B_production_rate_buffer = B_production_rate_current
            else:
                A_active_percent_current = A_active_percent
                B_current = B
                B_production_rate_current = B_production_rate
                A_active_percent_buffer = A_active_percent_current
                B_buffer = B_current
                B_production_rate_buffer = B_production_rate_current

            # Positive arm produce repressor
            theoretical_production = min(A * (A_active_percent_current / 100) * production_efficiency, maximum_production_rate)

            B_production_rate_change_amount = (theoretical_production - B_production_rate_current) * (production_change_rate / 100)
            B_change_amount = B_production_rate_current + max(delta_bacteria, 0)

            if simulate_desync:
                B_production_rate_change_amount *= random.gauss(1, desync_factor/100)
                B_change_amount *= random.gauss(1, desync_factor/100)

            B_production_rate_buffer += B_production_rate_change_amount
            B_buffer += B_change_amount

            # Negative arm repress positive arm
            theoretical_active = max(100 * (1 - (B_current * repression_efficiency/ A)), 0)

            A_active_percent_change = (theoretical_active - A_active_percent_current) * (repression_rate / 100)

            if simulate_desync:
                A_active_percent_change *= random.gauss(1, desync_factor/100)

            A_active_percent_buffer += A_active_percent_change

            # Negative arm degradation
            B_degradation_amount = B_buffer * (degradation_rate / 100)

            if simulate_desync:
                B_degradation_amount *= random.gauss(1, desync_factor/100)

            B_buffer -= B_degradation_amount

            # Push buffer to main variables

            if simulate_desync:
                A_active_percent_samples[i] = A_active_percent_buffer
                B_samples[i] = B_buffer
                B_production_rate_samples[i] = B_production_rate_buffer
            else:
                A_active_percent = A_active_percent_buffer
                B = B_buffer
                B_production_rate = B_production_rate_buffer

        previous_bacteria = bacteria

        # Write the current state to the output

        if current_step % save_step_interval == 0:

            if simulate_desync:
                # Take average of samples
                file.write(f"{current_step / 10},"
                           f"{sum(A_active_percent_samples)/desync_sampling},"
                           f"{sum(B_samples)/desync_sampling}\n")
            else:
                file.write(f"{current_step/10},"
                           f"{A_active_percent},"
                           f"{B}\n")

        current_step += 1
