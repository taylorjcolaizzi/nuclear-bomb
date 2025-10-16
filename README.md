# nuclear-bomb

Python coding project for nuclear physics 1 UVA.

How it works

Simple version

Make counter for neutrons, for energy. Define size of sphere, mean free path, cross-section/probability. This is what I have in my `tester.py` file. Works okay!

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