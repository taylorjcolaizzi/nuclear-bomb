# final project code for nuclear physics 1 with Dr. Cates
# My method of solving was ODEs and numerical solutions.

# import necessary modules
import tester_v2 # I made this!
import numpy as np
import matplotlib.pyplot as plt
import math

# This model depends primarily on the size of the bomb. This in turn determines the rate at which neutrons leave the spherical bomb.

# Find ejection probabilities based on radius and mfp
radii_to_test = [10, 15, 20, 25, 30]
uranium_density = 4.8*10**(22) # /cm^3
uranium_cross_section = 1.2 * 10**(-24) # cm^2

mean_free_path = -1/(uranium_cross_section * uranium_density) * math.log(1/2)
# print(mean_free_path)


fission_probability = math.exp(-uranium_cross_section * uranium_density * mean_free_path)
# print(fission_probability)
probability_to_eject = tester_v2.calculate_ejection_probabilities(radii_to_test, mean_free_path)

print('radii', radii_to_test)
print('fission probability', fission_probability)
print('eject probability', probability_to_eject)

# Test these ejection probabilities to see what happens
# Look at just 100 iterations of Euler Method ODE Solver

time_span = 10**(-6) # 1 µs
time_step = 10 * 10**(-9) # 10 ns
n_neutrons = 1
n_generations = 20

initial_state = [n_neutrons] # 100 starter neutrons
for i in range(n_generations - 1): # make room for more generations if needed.
    initial_state.append(0)

# now test!
for rad, prob in enumerate(probability_to_eject):
    test_state = initial_state # just to keep a backup.
    time, Generations, Exit = tester_v2.euler_chain_solver(test_state, 0, fission_probability, prob, time_span, time_step)
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
    plt.title('k_eff at radius ' + str(radii_to_test[rad]) + ' cm')
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()