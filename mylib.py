import numpy as np
import math
from numba import njit

# let's start by making our functions.
@njit
def k_number():
    """
    Returns :
    int: random int between 1 and 3
    """
    return round(np.random.rand() * 2 + 1)

@njit(fastmath = True, cache = True)
def mc_integrator3(N, radius, delta_size):
    """
    Uses monte carlo integration to calculate the probability that a random point inside a 3-dimensional sphere of radius radius will escape the sphere upon a small displacement of size delta_size.
    Parameters :
    TODO:
    Returns :
    TODO:
    """
    r2 = radius * radius

    # SOLID_ANGLE = 4 * np.pi
    # SPHERE_VOLUME = 4/3 * np.pi * radius ** 3
    
    count = 0

    for _ in range(N):
        while True:
            random_point = np.random.uniform(-radius, radius, 3)
            if (random_point * random_point).sum() <= r2:
                break
  
        random_vector = np.random.uniform(-1, 1, 3)
        random_vector2 = (random_vector * random_vector).sum()
        random_vector = random_vector / math.sqrt(random_vector2)

        new_position = random_point + random_vector * delta_size

        if (new_position * new_position).sum() > r2:
            count += 1

        # probability = count / (N * SOLID_ANGLE * SPHERE_VOLUME)
        probability = count / N

    return probability, count

@njit
def bomb_test(time, delta_time, generations, initial_neutrons, fission_rate, ejection_rate):
    neutron_storage = [0.0 for i in range(generations)]
    neutron_storage[0] = initial_neutrons

    for t in range(0, time, delta_time):
        neutron_storage[-1] = neutron_storage[-1] + ejection_rate * sum(neutron_storage[:-1])
        for i in range(generations - 1, 0, -1):
            neutron_storage[i] = neutron_storage[i] + neutron_storage[i - 1] * fission_rate * k_number() - neutron_storage[i] * ejection_rate - neutron_storage[i] * fission_rate
        neutron_storage[0] = neutron_storage[0] - neutron_storage[0] * ejection_rate - neutron_storage[0] * fission_rate
    
    return neutron_storage

@njit
def real_bomb_odes(state, fission_rate, ejection_rate):
    G1, G2, E = state
    dG1dt = -(fission_rate + ejection_rate) * G1
    dG2dt = (fission_rate * k_number()) * G1 - (fission_rate + ejection_rate) * G2
    dEdt = ejection_rate * (G1 + G2)
    return np.array([dG1dt, dG2dt, dEdt])

# @njit
def euler_real_bomb_solver(initial_conditions, fission_rate, ejection_rate, total_time, dt):
    G1i, G2i, Ei = initial_conditions
    t_start = 0.0
    t_final = total_time

    t = np.arange(t_start, t_final + dt, dt)
    num_steps = len(t)

    G1 = np.zeros(num_steps)
    G2 = np.zeros(num_steps)
    E = np.zeros(num_steps)

    G1[0], G2[0], E[0] = G1i, G2i, Ei

    for i in range(num_steps - 1):
        current_state = np.array([G1[i], G2[i], E[i]])
        derivatives = real_bomb_odes(current_state, fission_rate, ejection_rate)

        G1[i + 1] = G1[i] + dt * derivatives[0]
        G2[i + 1] = G2[i] + dt * derivatives[1]
        E[i + 1] = E[i] + dt * derivatives[2]

    return t, G1, G2, E