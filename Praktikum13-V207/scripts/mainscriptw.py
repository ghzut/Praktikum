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
D1M = np.array([15.80, 15.81, 15.80])/1000
D2M = np.array([15.63, 15.63, 15.63])/1000
M1M = np.array([4.96, 4.95, 4.97])/1000
M2M = np.array([4.45, 4.46, 4.45])/1000
delt1, delt2 = np.genfromtxt('scripts/Daten1', unpack=True)
Temp, deltTemp21, deltTemp22 = np.genfromtxt('scripts/Daten2', unpack=True)

# Werte mit Fehler
D1 = unp.uarray(np.mean(D1M), stats.sem(D1M))
D2 = unp.uarray(np.mean(D2M), stats.sem(D2M))
M1 = unp.uarray(np.mean(M1M), stats.sem(M1M))
M2 = unp.uarray(np.mean(M2M), stats.sem(M2M))
deltat1 = unp.uarray(np.mean(delt1), stats.sem(delt1))
deltat2 = unp.uarray(np.mean(delt2), stats.sem(delt2))
Temperatur = unp.uarray(np.mean(Temp), stats.sem(Temp))
var = []
for element in (deltTemp21, deltTemp22)
	var = np.mean(element[0]), stats.sem(element[1])
deltTemp2 = unp.uarray(var)
print(var)
print(deltTemp2)

#plt.plot(1/Temp, ) 





























# Graphen
timeK = np.linspace(-10, 60*(len(T1)-1)+10)

plt.clf()
plt.plot(t, T1, 'rx')
plt.plot(t, T2, 'b+')
plt.xlim(-10, 60*(len(T1)-1)+10)
plt.xlabel(r'$t/\si{\second}$')
plt.ylabel(r'$T/\si{\kelvin}$')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/T1T2')

plt.clf()
plt.plot(t, T1, 'rx')
plt.plot(timeK, poly2(timeK, unp.nominal_values(aVap), unp.nominal_values(bVap), unp.nominal_values(cVap)), 'b-')
plt.xlim(-10, 60*(len(T1)-1)+10)
plt.xlabel(r'$t/\si{\second}$')
plt.ylabel(r'$T_1/\si{\kelvin}$')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/T1')

plt.clf()
plt.plot(t, T2, 'rx')
plt.plot(timeK, poly2(timeK, unp.nominal_values(aKon), unp.nominal_values(bKon), unp.nominal_values(cKon)), 'b-')
plt.xlim(-10, 60*(len(T1)-1)+10)
plt.xlabel(r'$t/\si{\second}$')
plt.ylabel(r'$T_2/\si{\kelvin}$')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/T2')

durchT = np.linspace(1/T1[-1]-1/T1[0]*0.02, 1/T1[0]+1/T1[0]*0.02)
plt.clf()
plt.plot(1/T1, np.log(pb), 'rx')
plt.plot(durchT, line(durchT, *params), 'b-')
plt.xlim(1/T1[-1]-1/T1[0]*0.02, 1/T1[0]+1/T1[0]*0.02)
plt.xlabel(r'$T^{-1}/\si[per-mode=reciprocal]{\per\kelvin}$')
plt.ylabel(r'$\log(p_b/\si{\pascal})$')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/L')


