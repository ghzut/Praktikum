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

#[per-mode=reciprocal],[table-format=2.3,table-figures-uncertainty=1]

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

Kupfer= np.array(np.genfromtxt('scripts/Kupfer.txt',unpack=True))
Eisen = np.array(np.genfromtxt('scripts/Eisen.txt',unpack=True))
Nullabfall = (968+1034)/2000
def linear(a,x,b):
    return a*x+b

#Ausgleichsgeraden
punkte = np.linspace(0,Kupfer[0][-1]*1.1,1000)
lin = curve_fit(linear,Kupfer[0],np.log((Kupfer[2]/Kupfer[1])-Nullabfall),sigma = np.log(np.sqrt((Kupfer[2]/Kupfer[1])-Nullabfall)))
linfitsk = [lin[0],np.sqrt(np.diag(lin[1]))]
print("linearerFit,Kupfer:",linfitsk)
plt.cla()
plt.clf()
plt.plot(Kupfer[0],np.log((Kupfer[2]/Kupfer[1])-Nullabfall), 'gx', label='gemessene Werte')
plt.plot(punkte,linear(linfitsk[0][0],punkte,linfitsk[0][1]),label = 'linearer Fit')
plt.xlabel(r'$d/\si{\milli\meter}$')
plt.ylabel(r'$N/t\si{\per\second}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'Kupfer')

punkte = np.linspace(0,Eisen[0][-1]*1.1,1000)
lin = curve_fit(linear,Eisen[0],np.log((Eisen[2]/Eisen[1])-Nullabfall),sigma = np.log(np.sqrt(Eisen[2])/Eisen[1]))
linfitse = [lin[0],np.sqrt(np.diag(lin[1]))]
print("linearerFit,Eisen:",linfitse)

plt.cla()
plt.clf()
plt.plot(Eisen[0],np.log((Eisen[2]/Eisen[1])-Nullabfall), 'gx', label='gemessene Werte')
plt.plot(punkte,linear(linfitse[0][0],punkte,linfitse[0][1]),label = 'linearer Fit')
plt.xlabel(r'$d/\si{\milli\meter}$')
plt.ylabel(r'$N/t\si{\per\second}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'Eisen')
