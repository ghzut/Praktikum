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


#print(sum([1,2,3]))

Abmessungen=np.genfromtxt('scripts/zylinderdaten.txt')
ErsteMessung=np.genfromtxt('scripts/a.txt',unpack=True)
ZweiteMessung=np.genfromtxt('scripts/b.txt')
DritteMessung=np.genfromtxt('scripts/c.txt',unpack=True)
VierteMessung=np.genfromtxt('scripts/d.txt')

#Umrechnen
ErsteMessung=[ErsteMessung[0]/10**6, ErsteMessung[1], 10**(ErsteMessung[2]/20)]
ZweiteMessung=ZweiteMessung/10**6
DritteMessung=[(DritteMessung[0]+26.96)/10**6, DritteMessung[1], 10**(DritteMessung[2]/20)]


#berechnung der Schallgeschwindigkeiten
params=linregress(ErsteMessung[0],Abmessungen[0:-2]*2)
paramsGes1=unp.uarray(*params[0:-1])
print('Parameter bei der Berechnung der Schallgeschwindigkeit mit Impuls-Echo-Verfahren\n',paramsGes1)
params=linregress(ZweiteMessung,Abmessungen[0:-2])
paramsGes2=unp.uarray(*params[0:-1])
print('Parameter bei der Berechnung der Schallgeschwindigkeit mit Durchschallungs-Verfahren\n',paramsGes2)

#berechnung der Daempfungskonstanten
x=np.linspace(0.05,0.25)
params=linregress(Abmessungen[0:-2]*2,unp.log(ErsteMessung[1]/ErsteMessung[2]))
paramsDaempfung=unp.uarray(*params[0:-1])
print('Parameter bei der Berechnung der Daempfung mit Impuls-Echo-Verfahren\n',paramsDaempfung)
plt.cla()
plt.clf()
plt.plot(x, np.exp(unp.nominal_values(paramsDaempfung[1]))*np.exp(unp.nominal_values(paramsDaempfung[0]) *x), 'b-', label='Augleichsfunktion')
plt.plot(Abmessungen[0:-2]*2, (ErsteMessung[1]/ErsteMessung[2]), 'rx', label='Messwerte')
# plt.ylim(0, line(t[-1], *params)+0.1)
# plt.xlim(0, t[-1]*100)
# plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
# plt.ylabel(r'$\Delta f / \si{\hertz}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'test')


