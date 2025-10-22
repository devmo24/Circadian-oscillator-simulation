# Circadian oscillator simulation

This repository contains the Python script used to simulate a circadian oscillator in the paper, "An unrecognized host response to microbial exposure resets circadian timing." This code has been tested on Linux but should operate without issues on Windows and Mac. The packages `math` and `random` are required but should be bundled with a default installation of Python and therefore requires no further installation.

# Using the script
1. First, ensure that Python 3 is installed.
   * On Windows, download and install the latest version of Python 3 from https://www.python.org/downloads/
   * On Mac and Linux, Python 3 should be pre-installed. Go to the next step.
2. Download the code by clicking on the green "Code" button at the top of the repository page, then selecting "Download ZIP."
3. Once downloaded, extract the files from the compressed ZIP file.
4. Run the Python code.
   * On Windows, double click the file to run the script.
   * On Mac, double click the file to open the file. In the menu on the top of the screen, click on "Run" to run the script.
   * On Linux, the script can be run using terminal commands. First, locate where the file is. In the terminal, change the directory using the cd command so that working directory is where the file is (e.g. if the file is at ~/Downloads/Circadian-oscillator-simulation, then use this command: cd ~/Downloads/Circadian-oscillator-simulation/). Then, run the file using the following command: `python3 Simulation.py`.

# Modifying the simulation settings
All variables that control the simulation are listed at the top of the script:
```
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
simulate_desync = True
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
```
Internal variables that are used for calculations are listed below and should not be changed:
* All variables with the suffix `_buffer`
* previous_bacteria
* delta_bacteria
* current_step

Variables that can be changed:
* A is the initial abundance of Protein A
* A_active_percent is the initial percent of Protein A that is active and therefore producing Protein B
* B is the initial abundance of Protein B
* B_production_rate is the initial rate of production of Protein B
* bacteria is the initial amount of bacteria present. This variable is only used if the exposure is set to "stimulation."
* bacteria_add_time is the time (in steps) when the bacteria should be added. This variable is only used if the exposure is set to "stimulation."
* bacteria_to_add is the amount of bacteria to be added. This variable is only used if the exposure is set to "stimulation."
* exposure is the type of bacterial exposure to be simulated. This can be either "stimulation," which models a one-time addition of bacteria, or "oscillation," which models a continuous fluctuation of bacterial abundance
* simulate_desync controls whether desynchronization should be simulated. This can be either True or False
* desync_factor is the rate of desynchronization, given in percent. This variable is only used if simulate_desync is set to True
* desync_sampling is the sampling size of desynchronization. A greater number produces more accurate desynchronization simulations. This variable is only used if simulate_desync is set to True
* maximum_production_rate is the maximum production rate (per step) of Protein B
* production_efficiency is the ratio of how much Protein B can be made per step to the amount of active Protein A
* production_change_rate is the rate, in percent, at which the production rate of Protein B is changed per step
* degradation_rate is the rate, in percent, at which Protein B is degraded per step
* repression_efficiency is the ratio of how much Protein A is inactivated to the amount of Protein B
* repression_rate is the rate, in percent, at which Protein A is activated or inactivated per step
* steps is the number of steps to be simulated (1 step is 1/10th of an hour)
* save_step_interval is the interval at which data should be saved (e.g., an interval of 10 indicates that every 10th step should be saved)


