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

# unp.uarray(np.mean(), stats.sem())

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

# Messwerte

#Der erste Versuch 8a:
V1wo2_5 = np.genfromtxt('scripts/DatenV1', unpack=True)
print(V1wo2_5)
print("Die letzte Durchführung bei 2.5A")
V1ol2_5 = np.genfromtxt("scripts/DatenV1_2.5",unpack=True)
print(V1ol2_5)
#Der zweite Versuch 8c:
print("Der zweite Versuch")
V2 = np.genfromtxt("scripts/DatenV2")
print(V2)


#8a:
plt.plot(V1wo2_5[0], V1wo2_5[1], 'gx', label='Kennlinie mit I = 2,0 A')
plt.plot(V1wo2_5[0], V1wo2_5[2], 'g+', label='Kennlinie mit I = 2,1 A')
plt.plot(V1wo2_5[0], V1wo2_5[3], 'rx', label='Kennlinie mit I = 2,2 A')
plt.plot(V1wo2_5[0], V1wo2_5[4], 'r+', label='Kennlinie mit I = 2,3 A')
plt.plot(V1wo2_5[0], V1wo2_5[5], 'bx', label='Kennlinie mit I = 2,4 A')
plt.plot(V1ol2_5[0], V1ol2_5[1], 'yx', label='Kennlinie mit I = 2,5 A')
#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(0, t[-1]*100)
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$I / \si{\micro\ampere}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'Kennlinien')
plt.cla
plt.clf
