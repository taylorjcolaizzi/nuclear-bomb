# nuclear-bomb

Author: Taylor Colaizzi

Short Description: Supercritical uranium coding project for nuclear physics 1 at UVA.

## Background

When learning modern and nuclear physics in my undergraduate degree, we discussed the exponential decay of unstable nuclei. Although it's impossible to predict when an individual radioactive atom will decay, it's well understood that a large number of atoms of the same unstable isotope will reliably decrease in number at the same exponential decay rate. That is, the number of radioactive atoms at time $t$ follows the following equation:
$$N(t) = N_0*e^{-\lambda t}$$
where $N_0$ is the initial population of atoms and $\lambda$ is the decay constant. Interestingly, the statistics of the population is quite predictable; whereas, the statistics of individual nuclei is not so. I proceeded with the supercriticality project under this premise: **if I could describe how the populations of free neutrons and fission centers change over time, I might be able to accurately model a supercritical nuclear chain reaction!**

In my undergraduate computational physics course, we studied the Susceptible, Infected, Recovered (SIR) model of epidemiology. The SIR model attempts to describe the time evolution of a contagious disease as it spreads throughout a population. However, the SIR model is easily adapted to many other problems where different populations interact and their numbers change over time. The simplest SIR model comprises just three ordinary differential equations and tracks how a population of susceptible people $(S)$ become infected patients $(I)$ and eventually recover $(R)$ from their illnesses.
$$\frac{dS}{dt}(t) = -\beta S(t)I(t)$$
$$\frac{dI}{dt}(t) = \beta S(t)I(t) - \gamma I(t)$$
$$\frac{dR}{dt}(t) = \gamma I(t)$$
Here, the rate of change of each population depends on interactions with the other populations. These interactions are moderated by the coefficients $\beta$ and $\gamma$ that indicate the strength or rate of the interactions. The initial conditions usually consider $S_0=N-\delta$, $I_0=\delta$, and $R_0=0$ with $N$ as the total population and $\delta$ a small number of initially sick "patient zero" cases. As time progresses, the $S$ and $I$ populations intermingle, which pulls people from the $S$ camp into the $I$ camp. Simultaneously, time allows the infected patients $I$ to recover and transition into the recovered population $R$. The end-behavior of the evolution is steady-state with the entire population having gone through the infection-recovery process and is just $R_f=N$, $S_f=0$, and $I_f=0$.

ADD IMAGE OF sir MODEL HERE???



## How it works

Resources to look at 
Graph for cross section for U-235 -> has the graph on Wikipedia
https://en.wikipedia.org/wiki/Neutron_cross_section

Nuclear fission on Wikipedia
https://en.wikipedia.org/wiki/Nuclear_fission

What other scattering processes occur and their cross-sections?

How many neutrons are released from each fission, what is the energy distribution?

How much energy is released by each fission, how much variation?

If you include a neutron reflector, what are the relevant cross sections?

Assuming k = 2,

Can you find a value for k by looking at the variations of multiple single "seed" neutron calculations?

Can you estimate the fraction of U-235 that has fissioned when your device has produced energy equivalent to 15 kTons of TNT?

IDEAS FOR HOW TO MAKE THIS WORK!!!

You only need just a couple of interactions: neutron leaves sphere by scattering, neutron stays in sphere by scattering, neutron fissions with U-235, neutron gets absorbed. ~ need to figure out the energy after each interaction, or you won't be able tot get it realistic.

Pratik uses a class in python for Neutron(), which holds the generation, position, energy, interactions, and position. (I'm currently doing this with functions and stored variables in lists, not with classes.)

## References

- SIR Model: https://pmc.ncbi.nlm.nih.gov/articles/PMC8993010/