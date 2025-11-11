# final project code for nuclear physics 1 with Dr. Cates
# My method of solving was ODEs and monte carlo integration.

import library # I made this!
import matplotlib.pyplot as plt # graphing
import math # log, exp
import scipy # ODE integrator
import numpy # various linear algebra tools

# This model depends primarily on the size of the bomb. 
# This in turn determines the rate at which neutrons leave the spherical bomb.
# You may also specify the cross sections and the density, but these I've left
# as the default values for 1 MeV neutrons hitting U235

# Find ejection probabilities based on radius and mean free path
radii_to_test = numpy.linspace(1, 4, 2) # it explodes quickly!
volume_to_test = [4/3 * math.pi * r**3 for r in radii_to_test]
# print(radii_to_test)
# print(volume_to_test)

URANIUM_DENSITY = 4.8 * (10**(22)) # 1/cm^3
FISSION_CROSS_SECTION = 1.2 * (10**(-24)) # cm^2 at 1 MeV
ELASTIC_CROSS_SECTION = 6.7 * (10**(-24)) # cm^2 at 1 MeV
AVOGADRO_NUMBER = 6.022e23
AVOGADRO_NUMBER = 1.

# mean_free_path is average length before fission
fission_mean_free_path = -1/(FISSION_CROSS_SECTION * URANIUM_DENSITY) * math.log(1/2)
elastic_mean_free_path = -1/(ELASTIC_CROSS_SECTION * URANIUM_DENSITY) * math.log(1/2)
print(fission_mean_free_path, elastic_mean_free_path)
# scattering_centers = [URANIUM_DENSITY * v for v in volume_to_test]
scattering_centers = [(r / elastic_mean_free_path)**2 * 185 for r in radii_to_test]
print(scattering_centers)

fission_probability = math.exp(
    -FISSION_CROSS_SECTION * URANIUM_DENSITY * fission_mean_free_path
    )
elastic_probability = math.exp(
    -ELASTIC_CROSS_SECTION * URANIUM_DENSITY * elastic_mean_free_path
    )
print(fission_probability, elastic_probability)

probability_to_eject = library.calculate_ejection_probabilities(
    radii_to_test, 
    elastic_mean_free_path
    )

print('radii', radii_to_test)
print('fission probability', fission_probability)
print('eject probability', probability_to_eject)

TIME_SPAN = 1e-6 # 1 µs
TIME_STEP = 10e-9 # 10 ns
N_NEUTRONS = 185. # start with 185, got from book
N_NEUTRONS = 1.

# using the same method as the SIR_Example, but we have a more complicated state

# Initial conditions
I0 = N_NEUTRONS
R0 = 0.
P0 = 0.
S0 = scattering_centers[0]
N = AVOGADRO_NUMBER
N = 1000.

fission_rate = - math.log(1 - fission_probability) / (TIME_STEP)
print(fission_rate)


ejection_rate = - math.log(1e-10 if probability_to_eject[0] == 1 else 1 - probability_to_eject[0]) / (TIME_STEP)
print(ejection_rate)

t = numpy.linspace(0, TIME_SPAN, int(TIME_SPAN/TIME_STEP + 1))
print(t)

y0 = [S0/N, I0/N, R0/N, P0/N]
print(y0)

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
plt.xlabel('Time 10 ns', size = 16)
plt.ylabel("Number of Moles", size = 16)
plt.title('radius', size = 24)
plt.legend(fontsize = 16)
plt.grid(True)
plt.tight_layout()

plt.savefig('really_trying.jpg')
plt.show()

for i, r in enumerate(radii_to_test):
    S0 = scattering_centers[i]
    ejection_rate = - math.log(1e-10 if probability_to_eject[i] == 1 else 1-probability_to_eject[i])/TIME_STEP
    print('ejection rate', ejection_rate)

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
    plt.xlabel('Time 10 ns', size = 16)
    plt.ylabel("Number of Moles", size = 16)
    plt.title(f'radius = {r}', size = 24)
    plt.legend(fontsize = 16)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig('really_trying.jpg')
    plt.show()