import numpy as np

# setting some inital parameters
radius = 10
mfp = 1 # mean free path
k = 2

# need global variables, since we want to change it inside functions.
neutrons = 11 # initial neutrons. counts up and down as neutrons appear and go away
energy = 0 # initial energy. Just a counter for now
used = 0 # neutrons used up so far.

fiss_prob = 0.1
scat_prob = 1 - fiss_prob # currently unused

x, y, z = 0, 0, 0 # starting position of first neutron

def move(x, y, z):
    random_vector = np.random.rand(3) # get 3 random values for xyz
    unit_vector = random_vector / np.linalg.norm(random_vector) # normalize to 1 before scaling by mfp

    # add displacement to current position
    x += unit_vector[0] * mfp
    y += unit_vector[1] * mfp
    z += unit_vector[2] * mfp

    # return new position
    return x, y, z

def test_neutron(x, y, z):
    rnd_num = np.random.rand()
    global neutrons, energy, used # allow this function to modify these
    distance_from_center = np.sqrt(x**2 + y**2 + z**2) # r in spherical coordinates. Maybe a faster way to do this using numpy array?
    if distance_from_center > radius: # if outside bomb, remove neutron and reset next one
        print('at distance')
        neutrons -= 1
        x, y, z = 0., 0., 0.
        used += 1 # update the used count
        return True
    elif rnd_num < fiss_prob: # if inside bomb and fisses
        print('at fission')
        energy = energy + 1
        neutrons += k - 1 # one neutron got used up, but k new ones are created
        x, y, z = 0, 0, 0
        used += 1 # update the used count
        return True
    # else: # if inside bomb and no fission happens, just go again (scattering)
    #     pass
    return False

# running the program
print("running old method")
while neutrons:
    # move to a new position, then test for fission.
    x, y, z = move(x, y, z)
    if (test_neutron(x, y, z)): x, y, z = 0, 0, 0
print("energy:", energy)
print("used:", used)