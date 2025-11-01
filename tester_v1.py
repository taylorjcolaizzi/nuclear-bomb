import numpy as np

# setting some inital parameters
bomb_radius = 2
mean_free_path = 1 # mean free path
neutron_k = 2

# need global variables, since we want to change it inside functions.
neutron_count = 10 # initial neutrons. counts up and down as neutrons appear and go away
total_energy = 0 # initial energy. Just a counter for now
neutron_used = 0 # neutrons used up so far.

fiss_prob = 1/5

x, y, z = 0., 0., 0. # starting position of first neutron

def move(x, y, z):
    random_vector = np.random.rand(3) # get 3 random values for xyz
    unit_vector = random_vector / np.linalg.norm(random_vector) # normalize to 1 before scaling by mean_free_path

    # add displacement to current position


    x += unit_vector[0] * mean_free_path
    y += unit_vector[1] * mean_free_path
    z += unit_vector[2] * mean_free_path

    # return new position
    return x, y, z

def test_neutron(x, y, z):
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

# running the program
while neutron_used < 1000 and neutron_count > 0: # stop if we run out of neutrons or exceed 1000 used neutrons
    # move to a new position, then test for fission.
    x, y, z = move(x, y, z)
    if (test_neutron(x, y, z)): x, y, z = 0, 0, 0 # when true, reset position
print("total_energy:", total_energy)
print("neutron_used:", neutron_used)