from table import makeTable
from table import makeNewTable
from customFormatting import *
from linregress import linregress
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

def customExp(x, a, b, c):
	return a*np.exp(b/3600*x)+c #ACHTUNG!!!!!!!!! b/3600=-lambda

Nullmessung1 = 202/900
Nullmessung2 = 213/900

Indium = np.genfromtxt("scripts/Indium", unpack=True)
Rhodium = np.genfromtxt("scripts/Rhodium", unpack=True)
Indium = [Indium[0], [Indium[1]/240-Nullmessung1, np.sqrt(Indium[1]-Nullmessung1*240)/240]]
Rhodium = [Rhodium[0], [Rhodium[1]/15-Nullmessung2, np.sqrt(Rhodium[1]-Nullmessung2*15)/15]]



IndiumErgebnisse = linregress(Indium[0], np.log(Indium[1][0]))
print('Ergebnisse Indium',IndiumErgebnisse)

makeNewTable([Indium[0],Indium[1][0],Indium[1][1],np.log(Indium[1][0]),abs(np.log(Indium[1][0]+Indium[1][1])-np.log(Indium[1][0])),abs(np.log(Indium[1][0]-Indium[1][1])-np.log(Indium[1][0]))], r'{$t/\si{\second}$}&{$N$}&{$\sigma=\sqrt(N)$}&{$\ln(N)$}&{$\ln(N+\sigma)-\ln(N)$}&{$\ln(N)-\ln(N-\sigma)$}', 'Indium', [r'S[table-format=4.0]',r'S[table-format=1.1]',r'S[table-format=1.1]',r'S[table-format=1.2]',r'S[table-format=1.2]',r'S[table-format=1.2]'], [r'{:4.0f}',r'{:1.1f}',r'{:1.1f}',r'{:1.2f}',r'{:1.2f}',r'{:1.2f}'])

x = np.linspace(0, Indium[0][-1]*1.02, 10000)
plt.cla()
plt.clf()
plt.errorbar(Indium[0],np.log(Indium[1][0]),yerr=[abs(np.log(Indium[1][0]+Indium[1][1])-np.log(Indium[1][0])),abs(np.log(Indium[1][0]-Indium[1][1])-np.log(Indium[1][0]))], fmt='rx', label='Messwerte', visible=True)
plt.plot(x, IndiumErgebnisse[0][0]*x+IndiumErgebnisse[0][1], label='linearer Fit')
#plt.yscale(r'log')
#plt.ylim(0, line(t[-1], *params)+0.1)
plt.xlim(0, x[-1])
plt.xlabel(r'$t/\si{\second}$')
plt.ylabel(r'$\log(N)$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'IndiumLog')

T0 = 500
WerteGroesserT0 = Rhodium[0] >= T0
T1 = 200
WerteKleinerT1 = Rhodium[0] <= T1

x=Rhodium[0][WerteKleinerT1]
RhodiumErgebnisse1 = linregress(Rhodium[0][WerteGroesserT0], np.log(Rhodium[1][0][WerteGroesserT0]))
print('Ergebnisse 1 Rhodium',RhodiumErgebnisse1)
a1 = unp.uarray(RhodiumErgebnisse1[0][0],RhodiumErgebnisse1[1][0])
print('a1',a1)
RhodiumErgebnisse2 = linregress(Rhodium[0][WerteKleinerT1], np.log(Rhodium[1][0][WerteKleinerT1]))
a2 = unp.uarray(RhodiumErgebnisse2[0][0],RhodiumErgebnisse2[1][0])
print('Ergebnisse 2 Rhodium',RhodiumErgebnisse2)
print('a2',a2)
print('a2-a1',a2-a1)

makeNewTable([Rhodium[0],Rhodium[1][0],Rhodium[1][1],np.log(Rhodium[1][0]),abs(np.log(Rhodium[1][0]+Rhodium[1][1])-np.log(Rhodium[1][0])),abs(np.log(Rhodium[1][0]-Rhodium[1][1])-np.log(Rhodium[1][0]))], r'{$t/\si{\second}$}&{$N$}&{$\sigma=\sqrt(N)$}&{$\ln(N)$}&{$\ln(N+\sigma)-\ln(N)$}&{$\ln(N)-\ln(N-\sigma)$}', 'Rhodium', [r'S[table-format=3.0]',r'S[table-format=2.1]',r'S[table-format=1.1]',r'S[table-format=2.2]',r'S[table-format=1.2]',r'S[table-format=1.2]'], [r'{:3.0f}',r'{:4.1f}',r'{:1.1f}',r'{:5.2f}',r'{:1.2f}',r'{:1.2f}'])


x = np.linspace(0, Rhodium[0][-1]*1.02, 10000)
plt.cla()
plt.clf()
plt.errorbar(Rhodium[0],np.log(Rhodium[1][0]),yerr=[abs(np.log(Rhodium[1][0]+Rhodium[1][1])-np.log(Rhodium[1][0])),abs(np.log(Rhodium[1][0]-Rhodium[1][1])-np.log(Rhodium[1][0]))], fmt='rx', label='Messwerte', visible=True)
plt.plot(x, RhodiumErgebnisse1[0][0]*x+RhodiumErgebnisse1[0][1], label='linearer Fit der Werte für $t \ge' + str(T0) + r'\si{\second}$')
plt.plot(x, RhodiumErgebnisse2[0][0]*x+RhodiumErgebnisse2[0][1], label=r'linearer Fit der Werte für $t \le' + str(T1) + r'\si{\second}$')
#plt.yscale(r'log')
#plt.ylim(0, line(t[-1], *params)+0.1)
plt.xlim(0, x[-1])
plt.xlabel(r'$t/\si{\second}$')
plt.ylabel(r'$\log(N)$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'RhodiumLog')





