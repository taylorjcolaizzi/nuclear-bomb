import numpy as np

neutrons = 10
radius = 2
mfp = 1
energy = 0
fiss_prob = 0.1
scat_prob = 1 - fiss_prob
x, y, z = 0, 0, 0 # start position


# function to get random unit vector.
# function to test what happens to neutron after moving
# function to iterate over neutrons.

def move(x, y, z):
    random_vector = np.random.rand(3) # get 3 random values for xyz
    unit_vector = random_vector / np.linalg.norm(random_vector) # normalize to 1

    # add random_vector to current position
    # print(x, y, z, unit_vector)
    x += unit_vector[0] * mfp
    y += unit_vector[1] * mfp
    z += unit_vector[2] * mfp

    return x, y, z # return new position

def test_neutron(x, y, z):
    # allow this function to modify the global counters
    global neutrons, energy
    distance_from_center = np.sqrt(x**2 + y**2 + z**2) # r in spherical coordinates
    # print("at distance", distance_from_center)
    if distance_from_center > radius: # if outside bomb
        return 25
    elif np.random.rand() < fiss_prob: # if inside bomb and fisses
        return 1
    else: # if inside bomb and not fisses
        return -1

# now, we can start to run the program
while neutrons:
    print('neutrons:', neutrons, 'energy:', energy)
    # move to a new position, then test the neutron.
    x, y, z = move(x, y, z)
    result = test_neutron(x, y, z)
    if result == 25:
        neutrons -= 1 # neutron is gone
        x, y, z = 0, 0, 0 # reset position for next neutron
        print('escaped')
        pass
    elif result == 1:
        energy += 1 # add to energy count
        neutrons -= 1 # it gets used up
        neutrons += 2 # add 2 new neutrons. this is k value
        x, y, z = 0, 0, 0 # reset position for next neutron
        print('fissioned')
        pass # need to restart the loop
    else:
        print('scattered')