# final project code for nuclear physics 1 with Dr. Cates

import mylib

# example usage:
mylib.k_number()
mylib.mc_integrator3(1000, 1, .1)

# print(mylib.mc_integrator3(1000*1000, 10, 1))

mylib.bomb_test(40, 1, 6, 100, 0.1, 0.1)

mylib.real_bomb_odes([1, 2, 3], 0.1, 0.1)

initial_state = [100, 0, 0]
beta_value = 0.1
gamma_value = 0.1

time_span = 10**(-6)
time_step = 10 * 10**(-9)

# print(time_span, time_step)

time, S_values, I_values, R_values = mylib.euler_real_bomb_solver(initial_state, beta_value, gamma_value, time_span, time_step)

print(time, S_values, I_values, R_values)