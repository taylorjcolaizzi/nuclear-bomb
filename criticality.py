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

    # return new position and old mean_free_path
    return x, y, z, mean_free_path

def neutron_inside(x_final, y_final, z_final, bomb_radius):
    """
    Tests the position of a neutron to determine if it is still inside the bomb.
    Parameters:
    x_final, y_final, z_final : float, current coordinates of the neutron.
    bomb_radius : float, is radius of spherical bomb.
    Returns: Boolean
    True : neutron is still inside the bomb.
    False : neutron has escaped the bomb.
    """

    distance_from_center = np.sqrt(x_final**2, y_final**2, z_final**2)
    if distance_from_center > bomb_radius:
        return False # neutron left the bomb
    else:
        return True # neutron is still inside the bomb

def test_fission(fiss_prob):
    """
    Tests a neutron that's inside the bomb to determine if it fissions or not. Outputs the number of neutrons created as a result.
    Parameters:
    fiss_prob : float between 0 and 1, which is the probability of fission occurring when a neutron is inside the bomb.
    TODO : need to write a function that changes the fission probability, should be based on mean_free_path or something.
    TODO : nominally, this is always k = 2. But, we might want other values to add variety.
    Returns:
    neutron_k : int, which is number of neutrons added after the interaction.
    if neutron_k = 0, just had scattering.
    if neutron_k > 0 (= 2, basically), just had fission.
    """

    random_number = np.random.rand() # Monte Carlo for fission/scatter
    if random_number > fiss_prob: # no fission. scatter.
        neutron_k = 0
        return neutron_k
    else: # did fission, create 2 new neutrons.
        neutron_k = 2
        return neutron_k
    
# now that we have functions for moving neutrons, testing their position, and testing their fission, let's put together the program that runs this all.

# initial values
cross_section = 0.1
mean_free_path = 1
bomb_radius = 4
initial_neutrons = 10

# we gotta store the neutrons in a data structure like lists. Make the position and mean free path as lists.
current_generation = [] # place to store the neutrons' info
for n in range(initial_neutrons):
    current_generation.append([0, 0, 0, mean_free_path])

for n, neutron in enumerate(current_generation):
    current_generation[n] = [move_neutron(*neutron)] # * operator in python will "unpack" the list into its elements!
    # if neutron_inside
print(current_generation)