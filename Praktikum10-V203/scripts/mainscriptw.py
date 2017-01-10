from table import makeTable
from bereich import bereich
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp


# BackwardsVNominal = []
# BackwardsVStd = []
# for value in BackwardsV:
#     BackwardsVNominal.append(unp.nominal_values(value))
#     BackwardsVStd.append(unp.std_devs(value))
# BackwardsVNominal = np.array(BackwardsVNominal)
# BackwardsVStd = np.array(BackwardsVStd)

# makeTable([Gaenge, ForwardsVNominal*100, ForwardsVStd*100, BackwardsVNominal*100, BackwardsVStd*100], r'{'+r'Gang'+r'} & \multicolumn{2}{c}{'+r'$v_\text{v}/\si[per-mode=reciprocal]{\centi\meter\per\second}$'+r'} & \multicolumn{2}{c}{'+r'$v_\text{r}/\si[per-mode=reciprocal]{\centi\meter\per\second}$'+r'}', 'tabges', ['S[table-format=2.0]', 'S[table-format=2.3]', ' @{${}\pm{}$} S[table-format=1.3]', 'S[table-format=2.3]', ' @{${}\pm{}$} S[table-format=1.3]'], ["%2.0f", "%2.3f", "%2.3f", "%2.3f", "%2.3f"])


# plt.cla
# plt.clf
# plt.plot(ForwardsVNominal*100, DeltaVForwardsNominal, 'gx', label='Daten mit Bewegungsrichtung aufs Mikrofon zu')
# plt.plot(BackwardsVNominal*100, DeltaVBackwardsNominal, 'rx', label='Daten mit Bewegungsrichtung vom Mikrofon weg')
# plt.ylim(0, line(t[-1], *params)+0.1)
# plt.xlim(0, t[-1]*100)
# plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
# plt.ylabel(r'$\Delta f / \si{\hertz}$')
# plt.legend(loc='best')
# plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
# plt.savefig('build/'+'VgegenDeltaV')

# a = unp.uarray(params[0], np.sqrt(covar[0][0]))

T1, p1 = np.genfromtxt("Niedrigdruck", unpack=True)
T2, p2 = np.genfromtxt("Hochdruck", unpack=True)

T = np.append(T1, T2)
p = np.append(p1, p2)

def MessungNiedrig(T, L):
    return p_01*np.exp(-(L/R) * (1/T))

def MessungHoch(T, L):
    return p_02*np.exp(-(L/R) * (1/T))

def line(T, L):
    return

plt.cla
plt.clf
plt.plot(T, np.log(p), 'rx', label='Daten')
plt.ylim(0, line(t[-1], *params)+0.1)
plt.xlim(0, t[-1]*100)
plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
plt.ylabel(r'$\Delta f / \si{\hertz}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'logpgegenT')
