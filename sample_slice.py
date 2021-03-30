# -*- coding: utf-8 -*-
"""
Sample epitaxial design.
"""

from slice_1d import Layer, Slice

# GaAs n-contact
l1 = Layer('n-cont', 0.3e-4)
l1.set_parameter('Ev', 0)
l1.set_parameter('Ec', 1.424)
l1.set_parameter('Nd', 1e18)
l1.set_parameter('Na', 0)
l1.set_parameter('Nc', 4.7e17)
l1.set_parameter('Nv', 9.0e18)
l1.set_parameter('mu_n', 8000)
l1.set_parameter('mu_p', 370)
l1.set_parameter('tau_n', 2e-9)
l1.set_parameter('tau_p', 2e-9)
l1.set_parameter('B', 1e-10)
l1.set_parameter('Cn', 2e-30)
l1.set_parameter('Cp', 2e-30)
l1.set_parameter('eps', 12.9)
l1.set_parameter('n_refr', 3.493)
l1.set_parameter('g0', 1500)
l1.set_parameter('N_tr', 1.85e18)

# AlGaAs (x=0.4) n-cladding
l2 = Layer('n-clad', 1.5e-4)
l2.set_parameter('Ev', -0.2)
l2.set_parameter('Ec', 1.724)
l2.set_parameter('Nd', 5e17)
l2.set_parameter('Na', 0)
l2.set_parameter('Nc', 7.5e17)
l2.set_parameter('Nv', 1.2e19)
l2.set_parameter('mu_n', 800)
l2.set_parameter('mu_p', 100)
l2.set_parameter('tau_n', 2e-9)
l2.set_parameter('tau_p', 2e-9)
l2.set_parameter('B', 1e-10)
l2.set_parameter('Cn', 2e-30)
l2.set_parameter('Cp', 2e-30)
l2.set_parameter('eps', 11.764)
l2.set_parameter('n_refr', 3.351)
l2.set_parameter('g0', 0)
l2.set_parameter('N_tr', 2e7)

# AlGaAs (x=0.25) n-waveguide
l3 = Layer('n-wg', 0.5e-4)
l3.set_parameter('Ev', -0.125)
l3.set_parameter('Ec', 1.611)
l3.set_parameter('Nd', 1e17)
l3.set_parameter('Na', 0)
l3.set_parameter('Nc', 6.1e17)
l3.set_parameter('Nv', 1.1e19)
l3.set_parameter('mu_n', 3125)
l3.set_parameter('mu_p', 174)
l3.set_parameter('tau_n', 2e-9)
l3.set_parameter('tau_p', 2e-9)
l3.set_parameter('B', 1e-10)
l3.set_parameter('Cn', 2e-30)
l3.set_parameter('Cp', 2e-30)
l3.set_parameter('eps', 12.19)
l3.set_parameter('n_refr', 3.443)
l3.set_parameter('g0', 0)
l3.set_parameter('N_tr', 2e7)

# active region
l4 = Layer('active', 0.03e-4)
l4.set_parameter('Ev', 0)
l4.set_parameter('Ec', 1.424)
l4.set_parameter('Nd', 2e16)
l4.set_parameter('Na', 0)
l4.set_parameter('Nc', 4.7e17)
l4.set_parameter('Nv', 9.0e18)
l4.set_parameter('mu_n', 8000)
l4.set_parameter('mu_p', 370)
l4.set_parameter('tau_n', 2e-9)
l4.set_parameter('tau_p', 2e-9)
l4.set_parameter('B', 1e-10)
l4.set_parameter('Cn', 2e-30)
l4.set_parameter('Cp', 2e-30)
l4.set_parameter('eps', 12.9)
l4.set_parameter('n_refr', 3.493)
l4.set_parameter('g0', 1500)
l4.set_parameter('N_tr', 1.85e18)

# AlGaAs (x=0.25) p-waveguide
l5 = Layer('p-wg', 0.5e-4)  # AlGaAs x=0.25
l5.set_parameter('Ev', -0.125)
l5.set_parameter('Ec', 1.611)
l5.set_parameter('Nd', 0)
l5.set_parameter('Na', 1e17)
l5.set_parameter('Nc', 6.1e17)
l5.set_parameter('Nv', 1.1e19)
l5.set_parameter('mu_n', 3125)
l5.set_parameter('mu_p', 174)
l5.set_parameter('tau_n', 2e-9)
l5.set_parameter('tau_p', 2e-9)
l5.set_parameter('B', 1e-10)
l5.set_parameter('Cn', 2e-30)
l5.set_parameter('Cp', 2e-30)
l5.set_parameter('eps', 12.19)
l5.set_parameter('n_refr', 3.443)
l5.set_parameter('g0', 0)
l5.set_parameter('N_tr', 2e7)

# AlGaAs (x=0.4) p-cladding
l6 = Layer('p-clad', 1.5e-4)  # AlGaAs x=0.4
l6.set_parameter('Ev', -0.2)
l6.set_parameter('Ec', 1.724)
l6.set_parameter('Nd', 0)
l6.set_parameter('Na', 1e18)
l6.set_parameter('Nc', 7.5e17)
l6.set_parameter('Nv', 1.2e19)
l6.set_parameter('mu_n', 800)
l6.set_parameter('mu_p', 100)
l6.set_parameter('tau_n', 2e-9)
l6.set_parameter('tau_p', 2e-9)
l6.set_parameter('B', 1e-10)
l6.set_parameter('Cn', 2e-30)
l6.set_parameter('Cp', 2e-30)
l6.set_parameter('eps', 11.764)
l6.set_parameter('n_refr', 3.351)
l6.set_parameter('g0', 0)
l6.set_parameter('N_tr', 2e7)

# GaAs p-contact
l7 = Layer('p-cont', 0.3e-4)
l7.set_parameter('Ev', 0)
l7.set_parameter('Ec', 1.424)
l7.set_parameter('Nd', 0)
l7.set_parameter('Na', 2e18)
l7.set_parameter('Nc', 4.7e17)
l7.set_parameter('Nv', 9.0e18)
l7.set_parameter('mu_n', 8000)
l7.set_parameter('mu_p', 370)
l7.set_parameter('tau_n', 2e-9)
l7.set_parameter('tau_p', 2e-9)
l7.set_parameter('B', 1e-10)
l7.set_parameter('Cn', 2e-30)
l7.set_parameter('Cp', 2e-30)
l7.set_parameter('eps', 12.9)
l7.set_parameter('n_refr', 3.493)
l7.set_parameter('g0', 1500)
l7.set_parameter('N_tr', 1.85e18)

sl = Slice()
for l in [l1, l2, l3, l4, l5, l6, l7]:
    sl.add_layer(l)
