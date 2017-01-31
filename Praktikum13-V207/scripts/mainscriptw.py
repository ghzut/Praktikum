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
delt1M, delt2M = np.genfromtxt('scripts/Daten1', unpack=True)
TempM, deltTemp21M, deltTemp22M = np.genfromtxt('scripts/Daten2', unpack=True)
TempM += 273.15
Kkl = 0.07640/1000
DichteWasser = 998


# Werte mit Fehler
D1 = unp.uarray(np.mean(D1M), stats.sem(D1M))
D2 = unp.uarray(np.mean(D2M), stats.sem(D2M))
M1 = unp.uarray(np.mean(M1M), stats.sem(M1M))
M2 = unp.uarray(np.mean(M2M), stats.sem(M2M))
delt1 = unp.uarray(np.mean(delt1M), stats.sem(delt1M))
delt2 = unp.uarray(np.mean(delt2M), stats.sem(delt2M))
Temp = unp.uarray(np.mean(TempM), stats.sem(TempM))
var = []
varerr = []
for element in range(len(deltTemp21M)):
	var += [np.mean(np.append(deltTemp21M[element], deltTemp22M[element]))]
	varerr += [stats.sem(np.append(deltTemp21M[element], deltTemp22M[element]))]
deltTemp2 = unp.uarray(np.array(var), np.array(varerr))
deltTemp2M = unp.nominal_values(deltTemp2)

# Rechnung
Dichte1 = M1/(4/3*np.pi*(D1/2)**3)
Dichte2 = M2/(4/3*np.pi*(D2/2)**3)
print('Dichte1', Dichte1)
print('Dichte2', Dichte2)

Kgr = (Kkl *(Dichte1-DichteWasser)*delt1)/((Dichte2-DichteWasser)*delt2)
print('Kgr',Kgr)

def line(x, a, b):
	return a*x+b

params, covar = curve_fit(line, 1/TempM, np.log(deltTemp2M))
a = unp.uarray(params[0], np.sqrt(covar[0][0]))
b = unp.uarray(params[1], np.sqrt(covar[1][1]))
B = a
A = unp.exp(b)
print('A:', A)
print('B', B)

t = np.linspace(1/TempM[-1] - 1/TempM[0]*0.02, 1/TempM[0] + 1/TempM[0]*0.02)
plt.cla()
plt.clf()
plt.plot(1/TempM, np.log(deltTemp2M), 'rx', label='KP')
plt.plot(t, line(t,*params), 'b-', label='KP')
plt.xlim(1/TempM[-1] - 1/TempM[0]*0.02, 1/TempM[0] + 1/TempM[0]*0.02)
plt.xlabel(r'kp')
plt.ylabel(r'kp')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'tT')












