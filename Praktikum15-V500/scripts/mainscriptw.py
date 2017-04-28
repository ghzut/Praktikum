from table import makeTable
from linregress import linregress
from bereich import bereich
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp
import scipy.constants as const


# BackwardsVNominal = []
# BackwardsVStd = []
# for value in BackwardsV:
#     BackwardsVNominal.append(unp.nominal_values(value))
#     BackwardsVStd.append(unp.std_devs(value))
# BackwardsVNominal = np.array(BackwardsVNominal)
# BackwardsVStd = np.array(BackwardsVStd)

# makeTable([Gaenge, ForwardsVNominal*100, ForwardsVStd*100, BackwardsVNominal*100, BackwardsVStd*100], r'{'+r'Gang'+r'} & \multicolumn{2}{c}{'+r'$v_\text{v}/\si[per-mode=reciprocal]{\centi\meter\per\second}$'+r'} & \multicolumn{2}{c}{'+r'$v_\text{r}/\si[per-mode=reciprocal]{\centi\meter\per\second}$'+r'}', 'tabges', ['S[table-format=2.0]', 'S[table-format=2.3]', ' @{${}\pm{}$} S[table-format=1.3]', 'S[table-format=2.3]', ' @{${}\pm{}$} S[table-format=1.3]'], ["%2.0f", "%2.3f", "%2.3f", "%2.3f", "%2.3f"])


#makeTable([Array mit den einzelnen Messwertearrays], r'{ Überschrift } & ' ,'tabges' , ['S[table-format=2.0]', ] ,  ["%2.0f", ])

# unp.uarray(np.mean(), stats.sem())

# plt.cla()
# plt.clf()
# plt.plot(ForwardsVNominal*100, DeltaVForwardsNominal, 'gx', label='Messwerte mit Bewegungsrichtung aufs Mikrofon zu')
# plt.plot(BackwardsVNominal*100, DeltaVBackwardsNominal, 'rx', label='Messwerte mit Bewegungsrichtung vom Mikrofon weg')
# plt.ylim(0, line(t[-1], *params)+0.1)
# plt.xlim(0, t[-1]*100)
# plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
# plt.ylabel(r'$\Delta f / \si{\hertz}$')
# plt.legend(loc='best')
# plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
# plt.savefig('build/'+'VgegenDeltaV')

#funktionen
def std(x):
	return unp.std_devs(x)
def nom(x):
	return unp.nominal_values(x)


# gegebene Werte
Wellenlaengen = np.array([578, 546, 492, 435, 406, 365.5])*10**(-9)
c = const.value('speed of light in vacuum')
Frequenzen = c/Wellenlaengen


# Messwerte
gelb = np.genfromtxt("scripts/gelb", unpack=True)
gelb_alternativ = np.genfromtxt("scripts/gelb_alternativeDaten", unpack=True)
gruen = np.genfromtxt("scripts/gruen", unpack=True)
blaugruen = np.genfromtxt("scripts/blaugruen", unpack=True)
violett = np.genfromtxt("scripts/violett", unpack=True)
ultraV1 = np.genfromtxt("scripts/ultraV1", unpack=True)
ultraV2 = np.genfromtxt("scripts/ultraV2", unpack=True)

# In Standarteinheiten umwandeln
gelb[0] *= 10**(-3)
gelb[1] *= 10**(-12)
gelb_alternativ[0] *= 10**(-3)
gelb_alternativ[1] *= 10**(-12)
gruen[0] *= 10**(-3)
gruen[1] *= 10**(-12)
blaugruen[0] *= 10**(-3)
blaugruen[1] *= 10**(-12)
violett[0] *= 10**(-3)
violett[1] *= 10**(-12)
ultraV1[0] *= 10**(-3)
ultraV1[1] *= 10**(-12)
ultraV2[0] *= 10**(-3)
ultraV2[1] *= 10**(-12)

#a)
Nullstellen = []
params, covar = linregress(gelb[0][gelb[0]>=0][0:-1], np.sqrt(gelb[1][gelb[0]>=0][0:-1]))
params = unp.uarray(params, covar[0:-1])
Nullstelle = -params[1]/params[0]
Nullstellen += [Nullstelle]
print('Ugrenzgelb: ', Nullstelle)
plt.cla()
plt.clf()
plt.plot(gelb[0][gelb[0]>=0], np.sqrt(gelb[1][gelb[0]>=0])*10**6, r'yx', label='Messwerte')
x = np.linspace(-0.1, nom(Nullstelle)*1.02, 1000)
plt.plot(x, (nom(params[0])*x+nom(params[1]))*10**6, 'r', label='linearer Fit')
#plt.ylim(0, line(t[-1], *params)+0.1)
plt.xlim(x[0], x[-1])
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$\sqrt{I / \si{\pico\ampere}}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'sqrtIgegenUgelb')

params, covar = linregress(gruen[0][gruen[0]>=0][0:-1], np.sqrt(gruen[1][gruen[0]>=0][0:-1]))
params = unp.uarray(params, covar[0:-1])
Nullstelle = -params[1]/params[0]
Nullstellen += [Nullstelle]
print('Ugrenzgruen: ', Nullstelle)
plt.cla()
plt.clf()
plt.plot(gruen[0][gruen[0]>=0], np.sqrt(gruen[1][gruen[0]>=0])*10**6, r'x', c='#00ff00', label='Messwerte')
x = np.linspace(-0.1, nom(Nullstelle)*1.02, 1000)
plt.plot(x, (nom(params[0])*x+nom(params[1]))*10**6, 'r', label='linearer Fit')
#plt.ylim(0, line(t[-1], *params)+0.1)
plt.xlim(x[0], x[-1])
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$\sqrt{I / \si{\pico\ampere}}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'sqrtIgegenUgruen')

params, covar = linregress(blaugruen[0][blaugruen[0]>=0][0:-1], np.sqrt(blaugruen[1][blaugruen[0]>=0][0:-1]))
params = unp.uarray(params, covar[0:-1])
Nullstelle = -params[1]/params[0]
Nullstellen += [Nullstelle]
print('Ugrenzblaugruen: ', Nullstelle)
plt.cla()
plt.clf()
plt.plot(blaugruen[0][blaugruen[0]>=0], np.sqrt(blaugruen[1][blaugruen[0]>=0])*10**6, r'x', c='#00ffcc', label='Messwerte')
x = np.linspace(-0.1, nom(Nullstelle)*1.02, 1000)
plt.plot(x, (nom(params[0])*x+nom(params[1]))*10**6, 'r', label='linearer Fit')
#plt.ylim(0, line(t[-1], *params)+0.1)
plt.xlim(x[0], x[-1])
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$\sqrt{I / \si{\pico\ampere}}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'sqrtIgegenUblaugruen')

params, covar = linregress(violett[0][violett[0]>=0][0:-1], np.sqrt(violett[1][violett[0]>=0][0:-1]))
params = unp.uarray(params, covar[0:-1])
Nullstelle = -params[1]/params[0]
Nullstellen += [Nullstelle]
print('Ugrenzviolett: ', Nullstelle)
plt.cla()
plt.clf()
plt.plot(violett[0][violett[0]>=0], np.sqrt(violett[1][violett[0]>=0])*10**6, r'x', c='#cc33ff', label='Messwerte')
x = np.linspace(-0.1, nom(Nullstelle)*1.02, 1000)
plt.plot(x, (nom(params[0])*x+nom(params[1]))*10**6, 'r', label='linearer Fit')
#plt.ylim(0, line(t[-1], *params)+0.1)
plt.xlim(x[0], x[-1])
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$\sqrt{I / \si{\pico\ampere}}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'sqrtIgegenUviolett')

params, covar = linregress(ultraV1[0][ultraV1[0]>=0][0:-1], np.sqrt(ultraV1[1][ultraV1[0]>=0][0:-1]))
params = unp.uarray(params, covar[0:-1])
Nullstelle = -params[1]/params[0]
Nullstellen += [Nullstelle]
print('UgrenzultraV1: ', Nullstelle)
plt.cla()
plt.clf()
plt.plot(ultraV1[0][ultraV1[0]>=0], np.sqrt(ultraV1[1][ultraV1[0]>=0])*10**6, r'kx', label='Messwerte')
x = np.linspace(-0.1, nom(Nullstelle)*1.02, 1000)
plt.plot(x, (nom(params[0])*x+nom(params[1]))*10**6, 'r', label='linearer Fit')
#plt.ylim(0, line(t[-1], *params)+0.1)
plt.xlim(x[0], x[-1])
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$\sqrt{I / \si{\pico\ampere}}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'sqrtIgegenUultraV1')

params, covar = linregress(ultraV2[0][ultraV2[0]>=0][0:-1], np.sqrt(ultraV2[1][ultraV2[0]>=0][0:-1]))
params = unp.uarray(params, covar[0:-1])
Nullstelle = -params[1]/params[0]
Nullstellen += [Nullstelle]
print('UgrenzultraV2: ', Nullstelle)
plt.cla()
plt.clf()
plt.plot(ultraV2[0][ultraV2[0]>=0], np.sqrt(ultraV2[1][ultraV2[0]>=0])*10**6, r'kx', label='Messwerte')
x = np.linspace(-0.1, nom(Nullstelle)*1.02, 1000)
plt.plot(x, (nom(params[0])*x+nom(params[1]))*10**6, 'r', label='linearer Fit')
#plt.ylim(0, line(t[-1], *params)+0.1)
plt.xlim(x[0], x[-1])
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$\sqrt{I / \si{\pico\ampere}}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'sqrtIgegenUultraV2')

# b)
params, covar = linregress(Frequenzen, nom(Nullstellen))
params = unp.uarray(params, covar[0:-1])
print('h/e0 berechnet: ', params[0])
print('h/e0 lit: ', (const.value('Planck constant')/const.value('elementary charge')))
print('Austrittsarbeit in eV: ', -params[1])
plt.cla()
plt.clf()
plt.plot(Frequenzen, nom(Nullstellen), 'bx', label='Messwerte')
x = np.linspace(Frequenzen[0]-1000,  Frequenzen[-1]+1000, 1000)
plt.plot(x, (nom(params[0])*x+nom(params[1])), 'r', label='linearer Fit')
#plt.ylim(0, line(t[-1], *params)+0.1)
plt.xlim(x[0], x[-1])
plt.xlabel(r'$f/\si{\per\second}$')
plt.ylabel(r'$U_\text{g}/\si{\volt}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'Ugegennu')

# c)
plt.cla()
plt.clf()
plt.plot(gelb[0], gelb[1]*10**(9), 'yx', label='Messwerte')
#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(x[0], x[-1])
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$\sqrt{I / \si{\pico\ampere}}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'sqrtIgegenUgelb2')

# Alle Tabellen

# Werte-Tabellen
makeTable([gelb[0][0:len(gelb[0])//2+1]*10**3, gelb[1][0:len(gelb[1])//2+1]*10**12], r'{ $U/\si{\milli\volt}$ } & { $I/\si{\pico\ampere}$ }' ,'tabgelb1' , ['S[table-format=5.0]', 'S[table-format=4.0]'] ,  ["%5.0f", "%4.0f"])
makeTable([gelb[0][len(gelb[0])//2+1:]*10**3, gelb[1][len(gelb[1])//2+1:]*10**12], r'{ $U/\si{\milli\volt}$ } & { $I/\si{\pico\ampere}$ }' ,'tabgelb2' , ['S[table-format=5.0]', 'S[table-format=4.0]'] ,  ["%5.0f", "%4.0f"])

makeTable([gruen[0]*10**3, gruen[1]*10**12], r'{ $U/\si{\milli\volt}$ } & { $I/\si{\pico\ampere}$ }' ,'tabgruen' , ['S[table-format=3.0]', 'S[table-format=3.0]'] ,  ["%3.0f", "%3.0f"])

makeTable([blaugruen[0]*10**3, blaugruen[1]*10**12], r'{ $U/\si{\milli\volt}$ } & { $I/\si{\pico\ampere}$ }' ,'tabblaugruen' , ['S[table-format=3.0]', 'S[table-format=1.0]'] ,  ["%3.0f", "%1.0f"])

makeTable([violett[0]*10**3, violett[1]*10**12], r'{ $U/\si{\milli\volt}$ } & { $I/\si{\pico\ampere}$ }' ,'tabviolett' , ['S[table-format=3.0]', 'S[table-format=3.0]'] ,  ["%3.0f", "%3.0f"])

makeTable([ultraV1[0]*10**3, ultraV1[1]*10**12], r'{ $U/\si{\milli\volt}$ } & { $I/\si{\pico\ampere}$ }' ,'tabultraV1' , ['S[table-format=4.0]', 'S[table-format=2.0]'] ,  ["%4.0f", "%2.0f"])

makeTable([ultraV2[0]*10**3, ultraV2[1]*10**12], r'{ $U/\si{\milli\volt}$ } & { $I/\si{\pico\ampere}$ }' ,'tabultraV2' , ['S[table-format=4.0]', 'S[table-format=2.0]'] ,  ["%4.0f", "%2.0f"])

# Zwischenergebnis-Tabelle(n)
makeTable([Wellenlaengen*10**9, Frequenzen*10**(-12), nom(Nullstellen), std(Nullstellen)], r'{ $\lambda/\si{\nano\meter}$ } & { $f/\si[per-mode=reciprocal]{\per\pico\second}$ } & \multicolumn{2}{c}{ $U_\text{g}/\si{\volt}$ }' ,'tabZwischenErgebnisse' , ['S[table-format=3.1]', 'S[table-format=3.0]', 'S[table-format=1.2]', '@{${}\pm{}$}S[table-format=1.2]'] ,  ["%3.1f", "%3.0f", "%1.2f", "%1.2f"])

# Ergebnis-Tabelle (Es gibt keine!!!(unnötig meiner Ansicht nach!))























