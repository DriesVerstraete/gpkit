import numpy as np

import gpkit

pi = gpkit.Monomial("\\pi", value=np.pi)
CDA0 = gpkit.Monomial("(CDA0)", value=0.031)
rho = gpkit.Monomial("\\rho", value=1.23)
mu = gpkit.Monomial("\\mu", value=1.78e-5)
S_wetratio = gpkit.Monomial("(\\frac{S}{S_{wet}})", value=2.05)
k = gpkit.Monomial("k", value=1.2)
e = gpkit.Monomial("e", value=0.95)
W_0 = gpkit.Monomial("W_0", value=4940)
N_ult = gpkit.Monomial("N_{ult}", value=3.8)
tau = gpkit.Monomial("\\tau", value=0.12)
C_Lmax = gpkit.Monomial("C_{L,max}", value=1.5)
V_min = gpkit.Monomial("V_{min}")

D = gpkit.Monomial("D")
A = gpkit.Monomial("A")
S = gpkit.Monomial("S")
C_D = gpkit.Monomial("C_D")
C_L = gpkit.Monomial("C_L")
C_f = gpkit.Monomial("C_f")
Re = gpkit.Monomial("Re")
W = gpkit.Monomial("W")
W_w = gpkit.Monomial("W_w")
V = gpkit.Monomial("V")

substitutions = {}
equations = []

C_D_fuse = CDA0/S
C_D_wpar = k*C_f*S_wetratio
C_D_ind = C_L**2/(pi*A*e)
equations += [C_D >= C_D_fuse + C_D_wpar + C_D_ind]


W_w_strc = 8.71e-5*(N_ult*A**1.5*(W_0*W*S)**0.5)/tau
W_w_surf = 45.24*S
equations += [W_w >= W_w_surf + W_w_strc]

equations += [D >= 0.5*rho*S*C_D*V**2,
              Re <= (rho/mu)*V*(S/A)**0.5,
              C_f >= 0.074/Re**0.2,
              W <= 0.5*rho*S*C_L*V**2,
              W <= 0.5*rho*S*C_Lmax*V_min**2,
              W >= W_0 + W_w]


def single():
    substitutions.update({V_min: 22})
    return gpkit.GP(D, equations, substitutions)


def sweep():
    substitutions.update({
        V_min: ("sweep", np.linspace(20, 25, 10)),
        V: ("sweep", np.linspace(45, 55, 10)),
    })
    return gpkit.GP(D, equations, substitutions)