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


# Messing Schmal 9 x 0.7 x 0.4 93+-12
AMessingS = 0.09*0.007*0.004
pMessingS = 8520
cMessingS = 385
kMessingS = 93

# Messing Breit 9 x 1.2 x 0.4
AMessingB = 0.09*0.012*0.004
pMessingB = 8520
cMessingB = 385
kMessingB = 93

# Aluminium 9 x 1.2 x 0.4
AAluminium = 0.09*0.012*0.004
pAluminium = 2800
cAluminium = 380
kAluminium = 220

# Edelstahl 9 x 1.2 x 0.4
AEdlestahl = 0.09*0.012*0.004
pEdelstahl = 8000
cEdlestahl = 400
kEdelstahl = 20

# Abstand zwischen Thermoelementen an einem Stab
AbT = 0.03

# Hauptscript

x21, dT21 = np.genfromtxt("scripts/T2-T1", unpack=True)
x78, dT78 = np.genfromtxt("scripts/T7-T8", unpack=True)
x21, x78 = x21*1000/7.55, x78*1000/7.55

def line(x, a, b):
    return a*x+b

# Die zeitlichen Abstände berechnen
dx21 = []
dx21.append(x21[0])
for i in range(len(x21)-1):
    dx21.append(x21[i+1]-x21[i])
dx21 = np.array(dx21)
dx78 = []
dx78.append(x78[0])
for i in range(len(x78)-1):
    dx78.append(x78[i+1]-x78[i])
dx78 = np.array(dx78)

print('dT21/AbT:')
print(dT21/AbT)
print('dT78/AbT:')
print(dT78/AbT)
print('Wärmefluss T21')
print(-dT21/AbT * AMessingB *kMessingB)
print('Wärmefluss T78')
print(-dT78/AbT * AEdlestahl *kEdelstahl)

makeTable([x21, dT21, -dT21/AbT * AMessingB *kMessingB], r'{$t/\si{\second}$} & {$(T2-T1)/\si{\kelvin}$} & {$\frac{\Delta Q_\text{21}}{\Delta t}/\si{\watt}$}', 'tabT21', [r'S[table-format=4.0]', r'S[table-format=1.1]', r'S[table-format=0.3]'], ["%4.0f", "%1.1f", "%0.3f"])


# makeTable([T2[int(len(p2)/2):], p2[int(len(p2)/2):]/1000], r'{$T/\si{\kelvin}$} & {$p/\si{\kilo\pascal}$}', 'tab22', ['S[table-format=3.0]', 'S[table-format=3.0]'], ["%3.0f", "%3.0f"])
