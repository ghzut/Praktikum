from table import makeTable
from table import makeNewTable
from linregress import *
from customFormatting import *
from bereich import bereich
from weightedavgandsem import weighted_avg_and_sem
from weightedavgandsem import avg_and_sem
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

# einfacher:
# BackwardsVNominal = unp.nominal_values(BackwardsV)
# BackwardsVStd = unp.std_devs(BackwardsV)

# makeTable([Gaenge, ForwardsVNominal, ForwardsVStd, ], r'{Gang} & \multicolumn{2}{c}{$v_\text{v}/\si[per-mode=reciprocal]{\centi\meter\per\second}$} & ', 'name', ['S[table-format=2.0]', 'S[table-format=2.3]', ' @{${}\pm{}$} S[table-format=1.3]', ], ["%2.0f", "%2.3f", "%2.3f",])



# unp.uarray(np.mean(), stats.sem())
# unp.uarray(*avg_and_sem(values)))
# unp.uarray(*weighted_avg_and_sem(unp.nominal_values(bneuDiff), 1/unp.std_devs(bneuDiff)))

# plt.cla()
# plt.clf()
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
# params = unp.uarray(params, np.sqrt(np.diag(covar)))


# print('{}{}{}'.format(*convert(unp.uarray([1,2,3],[1,3,2]), unpFormat)))

Abmessungen=np.genfromtxt('scripts/zylinderdaten.txt')
ErsteMessung=np.genfromtxt('scripts/a.txt',unpack=True)
ZweiteMessung=np.genfromtxt('scripts/b.txt')
DritteMessung=np.genfromtxt('scripts/c.txt',unpack=True)
VierteMessung=np.genfromtxt('scripts/d.txt')

#Umrechnen
ErsteMessung=[ErsteMessung[0]/10**6, ErsteMessung[1], 10**((ErsteMessung[2])/20)]
ZweiteMessung=ZweiteMessung/10**6
DritteMessung=[(DritteMessung[0])/10**6, DritteMessung[1], 10**((DritteMessung[2])/20)]

#berechnungen

#   berechnung der Schallgeschwindigkeiten
params=linregress(ErsteMessung[0],Abmessungen[0:-2]*2)
Ges1Std=params[-1]
paramsGes1=unp.uarray(*params[0:-1])
print('Parameter bei der Berechnung der Schallgeschwindigkeit mit Impuls-Echo-Verfahren\n',paramsGes1, Ges1Std)
params=linregress(ZweiteMessung,Abmessungen[0:-2])
Ges2Std=params[-1]
paramsGes2=unp.uarray(*params[0:-1])
print('Parameter bei der Berechnung der Schallgeschwindigkeit mit Durchschallungs-Verfahren\n',paramsGes2, Ges2Std)

#   berechnung der Daempfungskonstanten
params=linregress(Abmessungen[0:-2]*2,unp.log(ErsteMessung[1]/ErsteMessung[2]))
paramsDaempfung=unp.uarray(*params[0:-1])
print('Parameter bei der Berechnung der Daempfung mit Impuls-Echo-Verfahren(Es sollte ca. 500 dB/m rauskommen)\n',paramsDaempfung*40/np.log(10))

#plots

#   plot von x gegen T1
x=np.linspace(0,ErsteMessung[0][-1]*1.02)
plt.cla()
plt.cla()
plt.clf()
plt.plot(x*10**6, unp.nominal_values(paramsGes1[1])+x*unp.nominal_values(paramsGes1[0]), 'b-', label='linearer Fit')
plt.plot(ErsteMessung[0]*10**6,Abmessungen[0:-2]*2, 'rx', label='Messwerte')
plt.xlim(x[0]*10**6, x[-1]*10**6)
plt.xlabel(r'$t/\si{\micro\second}$')
plt.ylabel(r'$x/\si{\meter}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'XgegenT1')

#   plot von x gegen T2
x=np.linspace(0,ZweiteMessung[-1]*1.02)
plt.cla()
plt.cla()
plt.clf()
plt.plot(x*10**6, unp.nominal_values(paramsGes2[1])+x*unp.nominal_values(paramsGes2[0]), 'b-', label='linearer Fit')
plt.plot(ZweiteMessung*10**6,Abmessungen[0:-2], 'rx', label='Messwerte')
plt.xlim(x[0]*10**6, x[-1]*10**6)
plt.xlabel(r'$t/\si{\micro\second}$')
plt.ylabel(r'$x/\si{\meter}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'XgegenT2')


#   plot von U gegen X
x=np.linspace(0.05,0.25)
plt.cla()
plt.clf()
plt.plot(x, unp.nominal_values(paramsDaempfung[1])+unp.nominal_values(paramsDaempfung[0]) *x, 'b-', label='linearer Fit')
plt.plot(Abmessungen[0:-2]*2, np.log(ErsteMessung[1]/ErsteMessung[2]), 'rx', label='Messwerte')
plt.xlim(x[0], x[-1])
plt.xlabel(r'$x/\si{\meter}$')
plt.ylabel(r'$\log(U/\si{\volt})$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'UgegenX')

#tabellen
#makeNewTable([Abmessungen], r'{$l/\si[per-mode=reciprocal]{\meter}$}','Abmessungen')
makeNewTable([convert(Abmessungen[0:-2], floatFormat, ['', '1.2E']),convert(ErsteMessung[0], floatFormat, ['', '1.2E']), convert(ErsteMessung[1], floatFormat, ['', '1.2E']), convert(ErsteMessung[2], floatFormat, ['', '1.2E'])], r'{$l/\si[per-mode=reciprocal]{\meter}$} & {$T/\si[per-mode=reciprocal]{\second}$} & {$U/\si[per-mode=reciprocal]{\volt}$} & {$U_\text{A}/U$}','a')
makeNewTable([convert(Abmessungen[0:-2], floatFormat, ['', '1.2E']),convert(ZweiteMessung, floatFormat, ['', '1.2E'])], r'{$l/\si[per-mode=reciprocal]{\meter}$} & {$T/\si[per-mode=reciprocal]{\second}$}','b')
makeNewTable([convert(DritteMessung[0], floatFormat, ['', '1.2E'])], r'{$\Delta T/\si[per-mode=reciprocal]{\second}$}','c')
makeNewTable([convert(VierteMessung, floatFormat, ['', '1.2E'])], r'{$T/\si[per-mode=reciprocal]{\second}$}','d')


