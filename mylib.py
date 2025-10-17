import numpy as np
import numba
from numba import njit

# let's start by making our functions.
def k_number():
    """
    Returns :
    int: random int between 1 and 3
    """
    return round(np.random.rand() * 2 + 1)

def mc_integrator3(N, radius, delta_size):
    """
    Uses monte carlo integration to calculate the probability that a random point inside a 3-dimensional sphere of radius radius will escape the sphere upon a small displacement of size delta_size.
    Parameters :
    TODO:
    Returns :
    TODO:
    """
    SOLID_ANGLE = 4 * np.pi
    SPHERE_VOLUME = 4/3 * np.pi * radius ** 3
    
    count = 0
    for point in range(N):
        random_point = np.random.uniform(size = 3) * 2 * radius - radius
        while np.linalg.norm(random_point) > radius:
            random_point = np.random.uniform(size = 3) * 2 * radius - radius
        
        random_vector = np.random.uniform(size = 3) * 2 - 1
        unit_vector = random_vector / np.linalg.norm(random_vector)
        delta_position = unit_vector * delta_size

        count += np.sum(np.linalg.norm(random_point + delta_position) > radius)

        probability = count / (N * SOLID_ANGLE * SPHERE_VOLUME)

    return probability, count