# final project code for nuclear physics 1 with Dr. Cates
# My method of solving was ODEs and numerical integration.

import library # I made this!
import matplotlib.pyplot as plt
import math
import scipy

# This model depends primarily on the size of the bomb. 
# This in turn determines the rate at which neutrons leave the spherical bomb.

# Find ejection probabilities based on radius and mfp
radii_to_test = [i for i in range(1,5, 5)] # list generation
uranium_density = 4.8 * (10**(22)) # 1/cm^3
uranium_cross_section = 1.2 * (10**(-24)) # cm^2

# mean_free_path is average length before fission
mean_free_path = -1/(uranium_cross_section * uranium_density) * math.log(1/2)
print(mean_free_path)

fission_probability = math.exp(
    -uranium_cross_section * uranium_density * mean_free_path
    )
print(fission_probability)

probability_to_eject = library.calculate_ejection_probabilities(radii_to_test, 
                                                                mean_free_path)

print('radii', radii_to_test)
print('fission probability', fission_probability)
print('eject probability', probability_to_eject)

# Test these ejection probabilities to see what happens
# Look at just 100 iterations of Euler Method ODE Solver

time_span = 10**(-6) # 1 µs
time_step = 10 * (10**(-9)) # 10 ns
n_neutrons = 1 * 1000 * 1 # start with 1000
n_generations = 20 # go up to 20 generations

initial_state = [n_neutrons] # starter neutrons
for i in range(n_generations - 1): # make room for more generations if needed.
    initial_state.append(0) # total length is n_generations

# now test!
for radius, probability in enumerate(probability_to_eject):
    test_state = initial_state # just to keep a backup.
    time, Generations, Exit = library.euler_chain_solver(test_state, 
                                                         0, 
                                                         fission_probability, 
                                                         probability, 
                                                         time_span, 
                                                         time_step)
    old_list = []
    older_list = []
    oldest_list = []
    for i in range(50, 100):
        new_list = []
        newer_list = []
        newest_list = []
        new_list.append(Generations[i][2] / Generations[i][1])
        newer_list.append(Generations[i][4] / Generations[i][3])
        newest_list.append(Generations[i][8] / Generations[i][7])
        old_list.append(sum(new_list) / len(new_list))
        older_list.append(sum(newer_list) / len(newer_list))
        oldest_list.append(sum(newest_list) / len(newest_list))
    plt.plot(old_list, linestyle = '-', label = 'between generations 2 and 1')
    plt.plot(older_list, linestyle = ':', label = '4 and 3')
    plt.plot(oldest_list, linestyle = '--', label = ' 8 and 7')
    plt.xlabel('time after 50 * 10 ns in ns')
    plt.ylabel('average k_eff of first half of generations')
    plt.title('k_eff at radius ' + str(radii_to_test[radius]) + ' cm')
    plt.grid()
    plt.legend()
    plt.tight_layout()
    # plt.show()

# now, let's do the same test but with the simple ODE method!
# uses "real_bomb_odes" function

# using the same method as the SIR_Example, but we have a more complicated state

# Initial conditions
N = 1000
I0 = 1
R0 = 0
P0 = 0
S0 = N - I0 - R0 - P0

fission_rate = - math.log(1 - 0.5) / (10e-9)
print(fission_rate)
ejection_rate = - math.log(1 - 0.6) / (10e-9)

import numpy
t = numpy.linspace(0, 1e-6, 101)
print(t)

y0 = [S0/N, I0/N, R0/N, P0/N]

solution = scipy.integrate.odeint(
    library.simple_bomb_odes, 
    y0, 
    t, 
    args = (fission_rate, ejection_rate)
    )
S, I, R, P = solution.T

plt.figure(figsize=(10,6))
plt.plot(t, S, label='Fission Centers', linestyle = '-', linewidth = 3)
plt.plot(t, I, label='Free Neutrons', linestyle = ':', linewidth = 3)
plt.plot(t, R, label='Escaped', linestyle = '--', linewidth = 3)
plt.plot(t, P, label='Total Fissions', linestyle = '-.', linewidth = 3)
plt.xlabel('Time (days)', size = 16)
plt.ylabel('Fraction of Population', size = 16)
plt.title('Example SIR Model with beta = 0.3 and gamma = 0.1', size = 24)
plt.legend(fontsize = 16)
plt.grid(True)
plt.tight_layout()

plt.savefig('really_trying.jpg')
plt.show()