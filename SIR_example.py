# code copied from copilot AI

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# SIR model differential equations
def sir_model(y, t, beta, gamma):
    S, I, R = y
    dS_dt = -beta * S * I
    dI_dt = beta * S * I - gamma * I
    dR_dt = gamma * I
    return [dS_dt, dI_dt, dR_dt]

# Initial conditions
N = 1000       # Total population
I0 = 1         # Initial number of infected individuals
R0 = 0         # Initial number of recovered individuals
S0 = N - I0 - R0  # Initial number of susceptible individuals

# Contact rate and mean recovery rate
beta = 0.3     # Infection rate
gamma = 0.1    # Recovery rate

# Time grid (in days)
t = np.linspace(0, 160, 160)

# Initial state vector
y0 = [S0/N, I0/N, R0/N]  # Normalize to fractions

# Integrate the SIR equations over the time grid
solution = odeint(sir_model, y0, t, args=(beta, gamma))
S, I, R = solution.T

# Plot the results
plt.figure(figsize=(10,6))
plt.plot(t, S, label='Susceptible', linestyle = '-', linewidth = 4)
plt.plot(t, I, label='Infected', linestyle = ':', linewidth = 4)
plt.plot(t, R, label='Recovered', linestyle = '--', linewidth = 4)
plt.xlabel('Time (days)')
plt.ylabel('Fraction of Population')
plt.title('SIR Model Simulation')
plt.legend()
plt.grid(True)
plt.show()