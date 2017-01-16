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
R = unp.uarray(8.3144598, 0.0000048)
eV = unp.uarray(1.6021766208, 0.0000000098)*10**(-19)
n = unp.uarray(6.022140857, 0.000000074)*10**23
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
plt.plot(1000/T1, np.log(p1), 'rx', label=r'Messwerte aus Messreihe für $p\le \SI{1}{\bar}$')
plt.plot(1000/T2, np.log(p2), 'gx', label=r'Messwerte aus Messreihe für $p> \SI{1}\bar$')
# plt.ylim(0,1)
# plt.xlim(T1[0], T2[-1]+2)
plt.xlabel(r'$T^{-1}/\si{\per\milli\kelvin}$')
plt.ylabel(r'$\log (p / \si{\pascal})$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'logpgegen1durchT')

t = np.linspace((1/T1[-1])*0.98, (1/T1[15])*1.02)
plt.cla()
plt.clf()
plt.plot(1000/T1[15:], np.log(p1[15:]), 'rx', label=r'Messwerte aus Messreihe für $p\le \SI{1}{\bar}$')
plt.plot(t*1000, line(t, *params), 'b-', label='linearer Fit')
# plt.ylim(0,1)
plt.xlim(t[0]*1000, t[-1]*1000)
plt.xlabel(r'$T^{-1}/\si{\per\milli\kelvin}$')
plt.ylabel(r'$\log (p / \si{\pascal})$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'logpgegen1durchTausgleich')


L = -a*R
print('L:', L)
print('Energie 1 kg Wasser:', L *1000/18)
La = R*373
print('La:', La)
Li = L - La
print('Li:', Li)
Lin = Li/(n*eV)
print('Li pro Molekül in eV', Lin)

def Polynom5(x, a5, a4, a3, a2, a1, a0):
    return Polynomn(x, [a0, a1, a2, a3, a4, a5])

def Polynom6(x, a6, a5, a4, a3, a2, a1, a0):
    return  Polynomn(x, [a0, a1, a2, a3, a4, a5, a6])

def Polynom3(x, a3, a2, a1, a0):
    return Polynomn(x, [a0, a1, a2, a3])

def Polynomn(x, params=[]):
    v = 0
    for i in range(len(params)):
        v = v + params[i]*x**i
    return v

#def Polynom5(x, a2, a1, a0):
#   return Polynomn(x, [a0, a1, a2])

#def Polynom6(x, a3, a2, a1, a0):
#    return Polynomn(x, [a0, a1, a2, a3])

params, covar = curve_fit(Polynom6, T2, p2)
print('params:', params)
print('covar:', covar)
var = np.sqrt(np.diag(covar))
print(var)
print('*:')
paramsableitung = []
varableitung = []
for i in range(len(params)):
    paramsableitung.append((len(params)-i-1)*params[i])
    varableitung.append((len(params)-i-1)*var[i])
paramsableitung = np.array(paramsableitung)[0:-1]
varableitung = np.array(varableitung)[0:-1]
print(paramsableitung)
print(varableitung)

t = np.linspace(T2[0]*0.98, T2[-1]*1.02)
plt.cla()
plt.clf()
plt.plot(T2, p2*10**-6, 'gx', label=r'Messwerte aus Messreihe für $p> \SI{1}\bar$')
plt.plot(t, Polynom6(t, *params)*10**-6, 'b-', label='Ausgleichspolynom 6. Grades')
# plt.ylim(0,1)
plt.xlim(t[0], t[-1])
plt.xlabel(r'$T/\si{\kelvin}$')
plt.ylabel(r'$p / \si{\mega\pascal}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'pgegenTausgleich')

makeTable([T1[0:int(len(p1)/4)], p1[0:int(len(p1)/4)]/1000], r'{$T/\si{\kelvin}$} & {$p/\si{\kilo\pascal}$}', 'tab11', ['S[table-format=3.1]', 'S[table-format=2.1]'], ["%2.1f", "%2.1f"])
makeTable([T1[int(len(p1)/4):int(2*len(p1)/4)], p1[int(len(p1)/4):int(2*len(p1)/4)]/1000], r'{$T/\si{\kelvin}$} & {$p/\si{\kilo\pascal}$}', 'tab12', ['S[table-format=3.1]', 'S[table-format=2.1]'], ["%2.1f", "%2.1f"])
makeTable([T1[int(2*len(p1)/4):int(3*len(p1)/4)], p1[int(2*len(p1)/4):int(3*len(p1)/4)]/1000], r'{$T/\si{\kelvin}$} & {$p/\si{\kilo\pascal}$}', 'tab13', ['S[table-format=3.1]', 'S[table-format=2.1]'], ["%2.1f", "%2.1f"])
makeTable([T1[int(3*len(p1)/4):], p1[int(3*len(p1)/4):]/1000], r'{$T/\si{\kelvin}$} & {$p/\si{\kilo\pascal}$}', 'tab14', ['S[table-format=3.1]', 'S[table-format=2.1]'], ["%2.1f", "%2.1f"])
makeTable([T2[0:int(len(p2)/2)], p2[0:int(len(p2)/2)]/1000], r'{$T/\si{\kelvin}$} & {$p/\si{\kilo\pascal}$}', 'tab21', ['S[table-format=3.0]', 'S[table-format=3.0]'], ["%3.0f", "%3.0f"])
makeTable([T2[int(len(p2)/2):], p2[int(len(p2)/2):]/1000], r'{$T/\si{\kelvin}$} & {$p/\si{\kilo\pascal}$}', 'tab22', ['S[table-format=3.0]', 'S[table-format=3.0]'], ["%3.0f", "%3.0f"])

T = np.linspace(T2[0]*0.98, T2[-1]*1.02, 1000)
R2 = unp.nominal_values(R)

#print(T)
#print((((R2*T)/(2*Polynom6(T, *params)))**2)-0.9/Polynom6(T, *params))
#print('R2:', R2)
#print('R2*T:', (R2*T))
#print(2*Polynom6(T, *params))
print(paramsableitung)

Tl, MM, MMM, Ll = np.genfromtxt("scripts/Literaturwerte", unpack=True)
Tl = Tl + 273.15
Ll=18*Ll
plt.cla()
plt.clf()
#plt.plot(T2, (R2*T2/(2*p2) + np.sqrt((R2*T2/(2*p2))**2-0.9/p2))*T2*Polynom5(T2, *paramsableitung), 'gx', label='mit orginal P')
plt.plot(T, ((R2*T)/(2*Polynom6(T, *params))+np.sqrt(((R2*T)/(2*Polynom6(T, *params)))**2-0.9/Polynom6(T, *params)))*T * Polynom5(T, *paramsableitung)/1000, 'b-', label='Genäherte Funktion von L')
plt.plot(Tl, Ll/1000, 'rx', label='Theoriewerte')
# plt.plot(T, ((R2*T)/(2*Polynom6(T, *params))+np.sqrt((R2*T)**2/(2*Polynom6(T, *params))**2-0.9/Polynom6(T, *params)))*T*1000, 'rx', label='Test' )
#plt.plot(T, Polynom5(T, *paramsableitung), 'g-', label='Genäherte Funktion von P.')
#plt.plot(T, (50.09-0.9298*T/1000-65.19*(T/1000)**2)*1000, 'y-', label='Literaturkurve')
#plt.plot(T, (R2*T/Polynom6(T, *params))*T*Polynom5(T, *paramsableitung), 'o-', label='allgemeine Gasgleichung')
plt.ylim(-20,140)
plt.xlim(T[0], T[-1])
plt.xlabel(r'$T/\si{\kelvin}$')
plt.ylabel(r'$L / \si{\kilo\joule\per\mol}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'LgegenT')

makeTable([Tl, Ll/1000], r'{$T/\si{\kelvin}$} & {$p/\si{\kilo\pascal\per\mol}$}', 'tab3', ['S[table-format=3.0]', 'S[table-format=2.3]'], ["%3.0f", "%2.3f"])
