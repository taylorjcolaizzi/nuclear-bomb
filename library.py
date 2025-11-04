import numpy as np
import math
from numba import njit

# @njit
def k_number():
    """
    Given that fission occured, determines number of product neutrons.

    Returns :
    int: random int between 2 and 3
    """
    return int(np.random.choice((2,3)))

@njit(fastmath = True, cache = True)
def mc_integrator3(N, radius, delta_size):
    """
    Monte Carlo (MC) integration to calculate the probability that a random
    point inside a 3-dimensional sphere of radius radius will escape the sphere
    upon a small displacement of size delta_size.
    Parameters :
    TODO:
    Returns :
    TODO:
    """
    r2 = radius * radius

    SOLID_ANGLE = 4 * np.pi
    SPHERE_VOLUME = 4/3 * np.pi * radius ** 3
    
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

        probability = count / (N * SOLID_ANGLE * SPHERE_VOLUME)
        # need to divide by all the length dimensions integrated over!

    return probability, count

@njit
def calculate_ejection_probabilities(radii, mean_step):
    """
    Calculates ejection probabilities using the average of 5 runs of
    mc_integrator3.
    Parameter :
    radii: list of radii to be tested
    mean_step: average length of neutron travel
    Returns :
    ejection_probabilities: a list of probabilities matching the radii inputted
    """
    ejection_probabilities = []
    for r in radii:
        print('testing r:', r)
        current_probability = []
        for i in range(5):
            probability, outside = mc_integrator3(1000*1000, r, mean_step)
            current_probability.append(probability)
        average_probability = sum(current_probability) / len(current_probability)
        ejection_probabilities.append(average_probability)
    
    return ejection_probabilities

@njit
def bomb_test(
    time,
    delta_time,
    generations,
    initial_neutrons,
    fission_rate,
    ejection_rate
    ):
    neutron_storage = [0.0 for i in range(generations)]
    neutron_storage[0] = initial_neutrons

    for t in range(0, time, delta_time):
        neutron_storage[-1] = (neutron_storage[-1] + 
                               ejection_rate * sum(neutron_storage[:-1]))
        for i in range(generations - 1, 0, -1):
            neutron_storage[i] = (neutron_storage[i] + 
                                  neutron_storage[i - 1] * fission_rate * k_number() - 
                                  neutron_storage[i] * ejection_rate - 
                                  neutron_storage[i] * fission_rate)
        neutron_storage[0] = (neutron_storage[0] - 
                              neutron_storage[0] * ejection_rate - 
                              neutron_storage[0] * fission_rate)
    
    return neutron_storage

def real_bomb_odes(state, fission_rate, ejection_rate):
    S, I, R = state
    dSdt = -(fission_rate) * S * I
    dIdt = (fission_rate * k_number()) * S * I - (ejection_rate) * I
    dRdt = ejection_rate * (I)
    return np.array([dSdt, dIdt, dRdt])

def euler_real_bomb_solver(initial_conditions, 
                           fission_rate, 
                           ejection_rate, 
                           total_time, 
                           dt):
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


def chain_odes(state, fission_rate, ejection_rate):
    """
    state: array of length N+1 -> [G1, G2, ..., GN, E]
    fission_rate: transition rate for generations
    ejection_rate: loss rate from each Gi into E
    """
    N = len(state) - 1
    G = state[:N] # stands for generations
    E = state[-1] # stands for exited neutrons

    dG = np.empty(N, dtype=float)

    # G1
    dG[0] = -(fission_rate + ejection_rate) * G[0]

    # G2..GN
    for i in range(1, N):
        dG[i] = (fission_rate * k_number() * G[i - 1] - 
                 (fission_rate + ejection_rate) * G[i])

    # E
    dE = ejection_rate * np.sum(G)

    return np.concatenate([dG, [dE]])

def euler_chain_solver(initial_conditions_minus_E, 
                       initial_conditions_only_E, 
                       fission_prob, 
                       ejection_prob, 
                       total_time, 
                       dt):
    """
    G0: array-like length N (initial values for G1..GN)
    E0: float (initial E)
    returns: t (T,), G (T,N), E (T,)
    """
    initial_conditions = np.asarray(initial_conditions_minus_E, dtype=float)
    N = len(initial_conditions)

    t = np.arange(0.0, total_time + dt, dt)
    T = len(t)

    Y = np.zeros((T, N + 1), dtype=float)
    Y[0, :N] = initial_conditions
    Y[0, -1] = initial_conditions_only_E

    fission_rate = fission_prob / dt
    ejection_rate = ejection_prob / dt

    for i in range(T - 1):
        dY = chain_odes(Y[i], fission_rate, ejection_rate)
        Y[i + 1] = Y[i] + dt * dY

    G = Y[:, :N]
    E = Y[:, -1]
    return t, G, E