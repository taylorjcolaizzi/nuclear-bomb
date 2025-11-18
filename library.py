import numpy as np
import math
from numba import njit

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

        # probability = count / (N * SOLID_ANGLE * SPHERE_VOLUME)

        probability = count / N # if you don't divide by dimension

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

def simple_bomb_odes(y, t, fission_rate, ejection_rate):
    """
    simple SIR model for examining the 
    number of free neutrons over time
    in the bomb simulation
    """
    S, I, R, P = y
    dSdt = -(fission_rate) * S * I
    # dIdt = (fission_rate * k_number()) * S * I - (ejection_rate) * I
    dIdt = (fission_rate) * 2.4 * S * I - ejection_rate * I
    dRdt = ejection_rate * (I)
    dPdt = fission_rate * S * I #counting the fissions, not neutrons produced!
    return [dSdt, dIdt, dRdt, dPdt]