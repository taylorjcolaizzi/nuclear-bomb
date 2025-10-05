import numpy as np

# this code is to find the critical mass of a nuclear bomb using monte carlo simulations.

# here are the functions we need to make this code work.

def move_neutron(x_initial, y_initial, z_initial, mean_free_path):
    """
    Calculates the new position of a neutron after moving the mean free path length in a random direction.
    Parameters:
    x_initial, y_initial, z_initial : float, which are the current coordinates of the neutron.
    Returns:
    x, y, z : float, which are the new coordinates of the neutron after moving.
    """

    random_vector = np.random.rand(3) # get 3 random values for xyz
    unit_vector = random_vector / np.linalg.norm(random_vector) # normalize to 1 before scaling by mean_free_path

    x = x_initial + unit_vector[0] * mean_free_path
    y = y_initial + unit_vector[1] * mean_free_path
    z = z_initial + unit_vector[2] * mean_free_path

    # return new position
    return x, y, z

def test_neutron(x_final, y_final, z_final, bomb_radius, fiss_prob, neutron_k):
    """
    Tests the position of a neutron to determine if it causes fission, escapes the bomb, or continues.
    Parameters:
    x_final, y_final, z_final : float, which are the current coordinates of the neutron.
    bomb_radius : float, which is the size of the spherical bomb.
    fiss_prob : float between 0 and 1, which is the probability of fission occurring when a neutron is inside the bomb.
    neutron_k : int, which is the number of neutrons produced per fission event.
    Returns: 0, 1, or 2, which indicate the outcome of the test. 0 for escape, 1 for fission, and 2 for continue.
    """
    rnd_num = np.random.rand()
    global neutron_count, total_energy, neutron_used # allow this function to modify these
    distance_from_center = np.sqrt(x**2 + y**2 + z**2) # r in spherical coordinates. Maybe a faster way to do this using numpy array?
    if distance_from_center > bomb_radius: # if outside bomb, remove neutron and reset next one
        neutron_count -= 1
        x, y, z = 0., 0., 0.
        neutron_used += 1 # update the used count
        return True
    elif rnd_num < fiss_prob: # if inside bomb and fisses
        total_energy = total_energy + 1
        neutron_count += neutron_k - 1 # one neutron got used up, but neutron_k new ones are created
        x, y, z = 0, 0, 0
        neutron_used += 1 # update the used count
        return True
    return False # function always returns a value