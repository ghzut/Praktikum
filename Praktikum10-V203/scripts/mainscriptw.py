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

T1, p1 = np.genfromtxt("scripts/Unterdruckmessung", unpack=True)
T2, p2 = np.genfromtxt("scripts/Uberdruckmessung", unpack=True)
p1 = p1*10**2
p2 = p2*10**5
T1 = T1+273.15
T2 = T2+273.15

def MessungNiedrig(T, L):
    return p_01*np.exp(-(L/R) * (1/T))

def MessungHoch(T, L):
    return p_02*np.exp(-(L/R) * (1/T))

def line(x, a, b):
    return a*x+b

params, covar = curve_fit(line, 1/T1[15:], np.log(p1[15:]))
a = unp.uarray(params[0], np.sqrt(covar[0][0]))
b = unp.uarray(params[1], np.sqrt(covar[1][1]))
print('a:', a)
print('b:', b)

plt.cla()
plt.clf()
plt.plot(1/T1, np.log(p1), 'rx', label='Daten1')
plt.plot(1/T2, np.log(p2), 'gx', label='Daten2')
# plt.ylim(0,1)
# plt.xlim(T1[0], T2[-1]+2)
plt.xlabel(r'$T^{-1}/\si{\per\kelvin}$')
plt.ylabel(r'$\log (p / \si{\pascal})$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'logpgegen1durchT')

t = np.linspace((1/T1[-1])*0.98, (1/T1[15])*1.02)
plt.cla()
plt.clf()
plt.plot(1/T1[15:], np.log(p1[15:]), 'rx', label='Daten1')
plt.plot(t, line(t, *params), 'b-', label='linearer Fit')
# plt.ylim(0,1)
plt.xlim(t[0], t[-1])
plt.xlabel(r'$T^{-1}/\si{\per\kelvin}$')
plt.ylabel(r'$\log (p / \si{\pascal})$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'logpgegen1durchTausgleich')

R = 1
L = a*R
def Polynom6(x, a6, a5, a4, a3, a2, a1, a0):
    return  Polynomn(x, [a0, a1, a2, a3, a4, a5, a6])
def Polynom3(x, a1, a2, a3, b):
    return Polynomn(x, [b, a3, a2, a1])

def Polynomn(x, params=[]):
    v = 0
    for i in range(len(params)):
        v = v + params[i]*x**i
    return v

params, covar = curve_fit(Polynom6, T2, p2)
print('params:', params)
print('covar:', covar)
print(np.sqrt(np.diag(covar)))

t = np.linspace(T2[0]*0.98, T2[-1]*1.02)
plt.cla()
plt.clf()
plt.plot(T2, p2, 'gx', label='Daten2')
plt.plot(t, Polynom6(t, *params), 'b-', label='Ausgleichspolynom 6. Grades')
# plt.ylim(0,1)
plt.xlim(t[0], t[-1])
plt.xlabel(r'$T/\si{\kelvin}$')
plt.ylabel(r'$p / \si{\pascal}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'pgegenTausgleich')

makeTable([T1[0:int(len(p1)/4)], p1[0:int(len(p1)/4)]], r'{$T/\si{\kelvin}$} & {$p/\si{\pascal}$}', 'tab11', ['S[table-format=2.1]', 'S[table-format=3.0]'], ["%2.1f", "%3.0f"])
makeTable([T1[int(len(p1)/4):int(2*len(p1)/4)], p1[int(len(p1)/4):int(2*len(p1)/4)]], r'{$T/\si{\kelvin}$} & {$p/\si{\pascal}$}', 'tab12', ['S[table-format=2.1]', 'S[table-format=3.0]'], ["%2.1f", "%3.0f"])
makeTable([T1[int(2*len(p1)/4):int(3*len(p1)/4)], p1[int(2*len(p1)/4):int(3*len(p1)/4)]], r'{$T/\si{\kelvin}$} & {$p/\si{\pascal}$}', 'tab13', ['S[table-format=2.1]', 'S[table-format=3.0]'], ["%2.1f", "%3.0f"])
makeTable([T1[int(3*len(p1)/4):], p1[int(3*len(p1)/4):]], r'{$T/\si{\kelvin}$} & {$p/\si{\pascal}$}', 'tab14', ['S[table-format=2.1]', 'S[table-format=3.0]'], ["%2.1f", "%3.0f"])
makeTable([T2[0:int(len(p2)/2)], p2[0:int(len(p2)/2)]], r'{$T/\si{\kelvin}$} & {$p/\si{\pascal}$}', 'tab21', ['S[table-format=2.1]', 'S[table-format=3.0]'], ["%2.1f", "%3.0f"])
makeTable([T2[int(len(p2)/2):], p2[int(len(p2)/2):]], r'{$T/\si{\kelvin}$} & {$p/\si{\pascal}$}', 'tab22', ['S[table-format=2.1]', 'S[table-format=3.0]'], ["%2.1f", "%3.0f"])

