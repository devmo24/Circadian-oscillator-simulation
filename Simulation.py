import math

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
bacteria_add_time = 550
bacteria_to_add = 300
exposure = "oscillation"

# Kinetic rates
maximum_production_rate = 100
production_efficiency = 5
production_change_rate = 0.5 # percent
degradation_rate = 4.96 # percent
repression_efficiency = 3
repression_rate = 2.8 # percent

steps = 20000
current_step = 0
save_step_interval = 10

with open("PER2 simulation.csv", "w") as file:
    file.write("Time,"
               "Active A (%),"
               "B\n")

    while current_step < steps:

        # Determine amount of bacteria

        # add bacteria once
        if exposure == "stimulation":
            if current_step == bacteria_add_time:
                bacteria = bacteria_to_add

        # bacterial exposure oscillates
        elif exposure == "oscillation":
            if current_step >= bacteria_add_time:
                bacteria = 30 + 25 * math.cos(((current_step/10) - 62) * 2 * math.pi / 24)

        delta_bacteria = bacteria - previous_bacteria

        # Positive arm produce repressor
        theoretical_production = min(A * (A_active_percent / 100) * production_efficiency, maximum_production_rate)
        B_production_rate_buffer += (theoretical_production - B_production_rate) * (production_change_rate / 100)
        B_buffer += B_production_rate + max(delta_bacteria, 0)

        # Negative arm repress positive arm
        theoretical_active = max(100 * (1 - (B * repression_efficiency/ A)), 0)
        A_active_percent_buffer += (theoretical_active - A_active_percent) * (repression_rate / 100)

        # Negative arm degradation
        B_buffer -= B_buffer * (degradation_rate / 100)

        # Push buffer to main variables
        A_active_percent = A_active_percent_buffer
        B = B_buffer
        B_production_rate = B_production_rate_buffer

        previous_bacteria = bacteria

        # Write the current state to the output

        if current_step % save_step_interval == 0:
            file.write(f"{current_step/10},"
                       f"{A_active_percent},"
                       f"{B}\n")

        current_step += 1
