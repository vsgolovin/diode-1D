# -*- coding: utf-8 -*-
"""
Class for storing all the parameters needed to simulate 1D semiconductor laser
operation.
"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.linalg import solve_banded
import units
import constants as const
from waveguide import solve_wg
import equilibrium as eq
import carrier_concentrations as cc

# DiodeData-specific necessary input parameters
input_params = ['Ev', 'Ec', 'Nd', 'Na', 'Nc', 'Nv', 'mu_n', 'mu_p', 'tau_n',
                'tau_p', 'B', 'Cn', 'Cp', 'eps', 'n_refr', 'g0', 'N_tr']
midp_params = ['Ev', 'Ec', 'Nc', 'Nv', 'mu_n', 'mu_p']
unit_values = {'Ev':units.E, 'Ec':units.E, 'Eg':units.E, 'Nd':units.n,
               'Na':units.n, 'C_dop':units.n, 'Nc':units.n, 'Nv':units.n,
               'mu_n':units.mu, 'mu_p':units.mu, 'tau_n':units.t,
               'tau_p':units.t, 'B':1/(units.n*units.t), 
               'Cn':1/(units.n**2*units.t), 'Cp':1/(units.n**2*units.t),
               'eps':1, 'n_refr':1, 'ni':units.n, 'wg_mode':1/units.x,
               'n0':units.n, 'p0':units.n, 'psi_lcn':units.V, 'psi_eq':units.V,
               'g0':1/units.x, 'N_tr':units.n}

class LaserData(object):

    def _calculate_values(self, device):
        self.values = dict()
        self.midp_values = dict()

        # input parameters at mesh nodes
        for p in input_params:
            self.values[p] = np.zeros_like(self.x)
            for i, xi in enumerate(self.x):
                self.values[p][i] = device.get_value(p, xi)
        # additional parameters
        self.values['Eg'] = self.values['Ec']-self.values['Ev']
        self.values['C_dop'] = self.values['Nd']-self.values['Na']
        self.values['ni'] = np.sqrt(self.values['Nc']*self.values['Nv']) \
                            * np.exp(-self.values['Eg'] / (2*self.Vt))

        # selected parameters at mesh midpoints
        for p in midp_params:
            self.midp_values[p] = np.zeros_like(self.xm)
            for i, xi in enumerate(self.xm):
                self.midp_values[p][i] = device.get_value(p, xi)

    def __init__(self, device, ar_ind, lam, L, w, R1, R2, ng, alpha_i,
                 beta_sp, step=1e-7, n_modes=3, remove_cl=True):
        params = device.get_params()
        assert all([p in params for p in input_params])
        assert device.ready

        # laser properties
        self.ar_ind = ar_ind
        self.lam = lam
        self.L = L
        self.w = w
        self.R1 = R1
        self.R2 = R2
        self.ng = ng
        self.vg = const.c / ng
        self.alpha_i = alpha_i
        self.alpha_m = 1/(2*L) * np.log(1/(R1*R2))
        self.beta_sp = beta_sp

        # generating uniform mesh
        d = device.get_thickness()
        self.x = np.arange(0, d, step)
        self.xm = (self.x[1:] + self.x[:-1]) / 2
        # boolean array for active region
        inds = np.array([device.get_index(xi) for xi in self.x])
        self.ar_ix = (inds==self.ar_ind)  # totally not confusing
        # constants and flags
        self.Vt = const.kb*const.T
        self.q = const.q
        self.eps_0 = const.eps_0
        self.fca_e = const.fca_e
        self.fca_h = const.fca_h
        self.is_dimensionless = False
        self.solved_lcn = False
        self.solved_equilibrium = False
        # calculating parameters' values
        self._calculate_values(device)

        # solving waveguide equation
        x = self.x.copy()
        n = self.values['n_refr']
        # removing narrow-gap contact layers
        if remove_cl:
            ind1 = device.inds[0]
            ind2 = device.inds[-1]
            ix = ~np.logical_or(inds==ind1, inds==ind2)
            x = x[ix]
            n = n[ix]
        n_eff, modes = solve_wg(x, n, lam, n_modes)

        # choosing mode with largest active region overlap
        inds = np.array([device.get_index(xi) for xi in x])
        ix = (inds==ar_ind)
        gammas = np.zeros(n_modes)
        for i in range(n_modes):
            mode = modes[:, i]
            gammas[i] = (mode*step)[ix].sum()
        i = np.argmax(gammas)
        self.n_eff = n_eff[i]
        self.values['wg_mode'] = modes[:, i]
        self.Gamma_f = interp1d(x, self.values['wg_mode'],
                                bounds_error=False, fill_value=0)
        self.Gamma_f_nd = interp1d(x/units.x, self.values['wg_mode']*units.x,
                                   bounds_error=False, fill_value=0)

    def generate_nonuniform_mesh(self, device, param='Eg', step_min=1e-7,
                                 step_max=20e-7, sigma=100e-7, y0=0, yn=0):
        def gauss(x, mu, sigma):
            return np.exp( -(x-mu)**2 / (2*sigma**2) )

        x = self.x.copy()
        y = self.values[param]

        # adding external values to y
        # same value as inside if y0 or yn is not a number
        if not isinstance(y0, (float, int)):
            y0 = y[0]
        if not isinstance(yn, (float, int)):
            yn = y[-1]
        y_ext = np.concatenate([np.array([y0]), y, np.array([yn])])

        # function for choosing local step size
        f = np.abs(y_ext[2:]-y_ext[:-2])  # change of y at every point
        fg = np.zeros_like(f)  # convolution for smoothing
        for i, xi in enumerate(x):
            g = gauss(x, xi, sigma)
            fg[i] = np.sum(f*g)
        fg_fun = interp1d(x, fg/fg.max())

        # creating new nonuniform grid
        new_grid = list()
        xi = 0
        while xi<=x[-1]:
            new_grid.append(xi)
            xi += step_min + (step_max-step_min)*(1-fg_fun(xi))
        self.x = np.array(new_grid)
        self.xm = (self.x[1:] + self.x[:-1]) / 2
        self._calculate_values(device)
        if self.is_dimensionless:
            self.values['wg_mode'] = self.Gamma_f_nd(self.x)
        else:
            self.values['wg_mode'] = self.Gamma_f(self.x)

        # new boolean array for active region
        inds = np.array([device.get_index(xi) for xi in self.x])
        self.ar_ix = (inds==self.ar_ind)

    def make_dimensionless(self):
        "Make every parameter dimensionless."
        assert not self.is_dimensionless

        # mesh
        self.x /= units.x
        self.xm /= units.x

        # parameters at mesh nodes and midpoints
        for p in self.values:
            self.values[p] /= unit_values[p]
        for p in self.midp_values:
            self.midp_values[p] /= unit_values[p]

        # laser diode parameters
        self.L /= units.x
        self.w /= units.x
        self.alpha_i /= 1/units.x
        self.alpha_m /= 1/units.x
        self.vg /= units.x/units.t

        # constants
        self.Vt /= units.E
        self.q /= units.q
        self.eps_0 = 1.0
        self.fca_e /= (units.x)**2
        self.fca_h /= (units.x)**2

        self.is_dimensionless = True

    def original_units(self):
        "Return from dimensionless to original units."
        assert self.is_dimensionless

        # mesh
        self.x *= units.x
        self.xm *= units.x

        # parameters at mesh nodes and midpoints
        for p in self.values:
            self.values[p] *= unit_values[p]
        for p in self.midp_values:
            self.midp_values[p] *= unit_values[p]

        # laser diode parameters
        self.L *= units.x
        self.w *= units.x
        self.alpha_i *= 1/units.x
        self.alpha_m *= 1/units.x
        self.vg *= units.x/units.t

        # constants
        self.Vt *= units.E
        self.q *= units.q
        self.eps_0 = const.eps_0
        self.fca_e *= (units.x)**2
        self.fca_h *= (units.x)**2

        self.is_dimensionless = False

    def solve_lcn(self, n_iter=20, lam=1.0, delta_max=1e-8):
        "Find built-in potential assuming local charge neutrality."
        C_dop = self.values['C_dop']
        Nc = self.values['Nc']
        Nv = self.values['Nv']
        Ec = self.values['Ec']
        Ev = self.values['Ev']
        Vt = self.Vt
        self.values['psi_lcn'] = eq.Ef_lcn_fermi(C_dop, Nc, Nv, Ec, Ev, Vt,
                                                 n_iter, lam, delta_max)
        self.solved_lcn = True

    def solve_equilibrium(self, n_iter=3000, lam=1.0, delta_max=1e-6):
        "Solve Poisson's equation at equilibrium."
        x = self.x
        xm = self.xm
        q = self.q
        eps_0 = self.eps_0
        eps = self.values['eps']
        C_dop = self.values['C_dop']
        Nc = self.values['Nc']
        Nv = self.values['Nv']
        Ec = self.values['Ec']
        Ev = self.values['Ev']
        Vt = self.Vt

        # psi_lcn -- initial guess for built-in potential
        if not self.solved_lcn:
            self.solve_lcn()
        psi = self.values['psi_lcn'].copy()

        # Newton's method
        self.delta = np.zeros(n_iter)  # change in psi
        for i in range(n_iter):
            A = eq.poisson_jac(psi, x, xm, eps, eps_0, q,
                               C_dop, Nc, Nv, Ec, Ev, Vt)
            b = eq.poisson_res(psi, x, xm, eps, eps_0, q,
                               C_dop, Nc, Nv, Ec, Ev, Vt)
            dpsi = solve_banded((1, 1), A, -b)
            self.delta[i] = np.mean(np.abs(dpsi))
            psi[1:-1] += lam*dpsi

        # storing solution and equilibrium concentrations
        assert self.delta[-1]<delta_max
        self.values['psi_eq'] = psi
        self.values['n0'] = cc.n(psi, 0, Nc, Ec, Vt)
        self.values['p0']= cc.p(psi, 0, Nv, Ev, Vt)
        self.solved_equilibrium = True


if __name__=='__main__':
    import matplotlib.pyplot as plt
    from sample_laser import sl
    ld = LaserData(sl, 3, 0.87e-4, 0.2, 0.01, 0.3, 0.3, 3.8, 1.0, 1e-5)
    ld.generate_nonuniform_mesh(sl)
    ld.make_dimensionless()

    plt.figure("Sample laser / %d mesh points"%(len(ld.x)))
    plt.plot(ld.x, ld.Gamma_f_nd(ld.x), label=ld.n_eff, c='k')
    plt.xlabel('Coordinate')
    plt.ylabel('Vertical mode profile')
    plt.twinx()
    plt.plot(ld.x, ld.values['Eg'], c='b')
    plt.ylabel('Bandgap', c='b')