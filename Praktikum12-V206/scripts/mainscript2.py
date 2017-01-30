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

# Werte
R = unp.uarray(8.3144598, 0.0000048) # J/(mol*K)
cWasser = 4183 #J/(K*kg)
MasseWasserInEimer = 3 # kg
CEimer = 660 # J/K
k = 1.14
rho0 = 5.51 # g/l = kg/m^3 bei 
T0 = 273.15 # K und 
p0 = 10**5 # Pa

pa, pb, T1, T2, N= np.genfromtxt("scripts/Daten", unpack=True)
pa += 1
pb += 1
pa *= 10**5
pb *= 10**5
T1 += 273.15
T2 += 273.15
t = np.linspace(0, 60*(len(T1)-1), len(T1))

# Rechnung
def poly2(x, a, b, c):
	return a*x**2+b*x+c

paramsKon, covarKon = curve_fit(poly2, t, T2)
aKon = unp.uarray(paramsKon[0], np.sqrt(covarKon[0][0]))
bKon = unp.uarray(paramsKon[1], np.sqrt(covarKon[1][1]))
cKon = unp.uarray(paramsKon[2], np.sqrt(covarKon[2][2]))
paramsVap, covarVap = curve_fit(poly2, t, T1)
aVap = unp.uarray(paramsVap[0], np.sqrt(covarVap[0][0]))
bVap = unp.uarray(paramsVap[1], np.sqrt(covarVap[1][1]))
cVap = unp.uarray(paramsVap[2], np.sqrt(covarVap[2][2]))
print('Kon')
print(aKon, bKon)
print('Vap')
print(aVap, bVap)

def line(x, a, b):
	return a*x+b

def dT1dt(x):
	return 2*aVap*x+bVap

def dT2dt(x):
	return 2*aKon*x+bKon

def dQ1dt(x):
	return (CEimer+MasseWasserInEimer*cWasser)*dT1dt(x)

def dQ2dt(x):
	return (CEimer+MasseWasserInEimer*cWasser)*dT2dt(x)

v = dQ1dt(t)[1:]/N[1:]
print('v')
print(v)

params, covar = curve_fit(line, 1/T1, np.log(pb))
a = unp.uarray(params[0], np.sqrt(covar[0][0]))
L = -a*R*1000/18 # J/(kg*K)
# L = unp.uarray(22002.332, 318.11)*1000/18
# L = 167190
print('L')
print(L)

dmdt = dQ2dt(t)/L
print('dmdt')
print(dmdt)

def rho(pa, T2):
	return rho0*T0*pa/(T2*p0)

Nmech = 1/(k-1)*(pb*(pa/pb)**(1/k) -pa)*(1/rho(pa, T2))*dmdt
print('Nmech')
print(Nmech)





































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


