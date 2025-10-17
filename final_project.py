# final project code for nuclear physics 1 with Dr. Cates
# My method of solving was ODEs and numerical solutions.
import mylib
import numpy as np

# This model depends primarily on the size of the bomb. This in turn determines the rate at which neutrons leave the spherical bomb.

# Find ejection probabilities based on radius and mfp
radii_to_test = [1, 5, 10, 15, 20]
mean_free_path = 0.1
probability_to_eject = mylib.calculate_ejection_probabilities(radii_to_test, mean_free_path)

print('radii', radii_to_test)
print('probs', probability_to_eject)

# Test these ejection probabilities to see what happens
# Look at just 100 iterations of Euler Method ODE Solver

time_span = 10**(-6) # 1 µs
time_step = 10 * 10**(-9) # 10 ns
n_neutrons = 100
n_generations = 10

initial_state = [n_neutrons] # 100 starter neutrons
for i in range(n_generations): # make room for 10 generations if needed.
    initial_state.append(0)
for prob in probability_to_eject:
    test_state = initial_state
    time, Generations, Exit = mylib.euler_chain_solver(test_state, 0, .1, prob, time_span, time_step)
    print('got data for prob:', prob)
    for i in range(99, 100):
        print('printing for prob:', prob)
        print(Generations[i].round(), Exit[i].round())
        print(round(sum(Generations[i])), round(Exit[i]))

# Let's examine k_eff for each of these generations. k_eff is neutrons in current generation divided by neutrons in previous generation.
