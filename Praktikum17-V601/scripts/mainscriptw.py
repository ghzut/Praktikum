from table import makeTable
from bereich import bereich
from weightedavgandstd import weighted_avg_and_std
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


#makeTable([Array mit den einzelnen Datenarrays], r'{'+r'Überschrift'+r'} & ' ,'tabges' , ['S[table-format=2.0]', ] ,  ["%2.0f", ])

# unp.uarray(np.mean(), stats.sem())

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

#0. Konstanten
a2Asymtote = 1.3


#1. Messwerte einlesen
#	x-AchsenFaktor berechnen
a1xAchseAbstände = np.genfromtxt('scripts/a1', unpack=True) #Abstand in cm zwischen 1 Volt Abständen
a1xAchseFaktor = 1/unp.uarray(np.mean(a1xAchseAbstände), stats.sem(a1xAchseAbstände)) # Anzahl der Volt pro cm
a2xAchseAbstände = np.genfromtxt('scripts/a2', unpack=True) #Abstand in cm zwischen 1 Volt Abständen
a2xAchseFaktor = 1/unp.uarray(np.mean(a2xAchseAbstände), stats.sem(a2xAchseAbstände)) # Anzahl der Volt pro cm
bxAchseAbstände = np.genfromtxt('scripts/b', unpack=True) #Abstand in cm zwischen 5 Volt Abständen
bxAchseFaktor = 5/unp.uarray(np.mean(bxAchseAbstände), stats.sem(bxAchseAbstände)) # Anzahl der Volt pro cm
cxAchseAbstände = np.genfromtxt('scripts/c', unpack=True) #Abstand in cm zwischen 5 Volt Abständen
cxAchseFaktor = 5/unp.uarray(np.mean(cxAchseAbstände), stats.sem(cxAchseAbstände)) # Anzahl der Volt pro cm

#   Differenzen der Maxima in b
bDiff = np.genfromtxt('scripts/bDiff', unpack=True)*bxAchseFaktor
bDiff = unp.uarray(*weighted_avg_and_std(unp.nominal_values(bDiff), unp.std_devs(bDiff)))


#	x/y-Koordinaten; x-Achse in 1Volt
a1Koordinaten = np.genfromtxt('scripts/SteigungsDreiecke', unpack=True)
a1Koordinaten = [a1Koordinaten[0]*a1xAchseFaktor, a1Koordinaten[1]]
a2Koordinaten = np.genfromtxt('scripts/a2Punkte', unpack=True)
a2Koordinaten = [a2Koordinaten[0]*a2xAchseFaktor, a2Koordinaten[1]]
cKoordinaten = np.genfromtxt('scripts/cPunkte', unpack=True)
cKoordinaten = [cKoordinaten[0]*cxAchseFaktor, cKoordinaten[1]]

#   Steigungen berechnen von a1
AbleitungVona1 = []
for i in range(len(a1Koordinaten[0][0:-1])):
    AbleitungVona1.append([(a1Koordinaten[0][i]+a1Koordinaten[0][i+1])/2, (a1Koordinaten[1][i+1]-a1Koordinaten[1][i])/(a1Koordinaten[0][i+1]-a1Koordinaten[0][i])])
AbleitungVona1 = np.array(AbleitungVona1).T


#2. Fits fitten
def line(x, a, b):
    return a*x+b

params, covar = curve_fit(line, *unp.nominal_values(a2Koordinaten))
a2params = unp.uarray(params, np.sqrt(np.diag(covar)))
params, covar = curve_fit(line, *unp.nominal_values(cKoordinaten))
cparams = unp.uarray(params, np.sqrt(np.diag(covar)))

#3. Ausgabe
print('bDiff:', bDiff)

#4.  Plots
#   a1
plt.cla()
plt.clf()
plt.plot(*unp.nominal_values(AbleitungVona1), 'rx', label='a1Ableitung')
#plt.plot(x, line(x, *unp.nominal_values(a2params)), 'b-', label='a2fit')
#plt.ylim(0, line(x[-1], *unp.nominal_values(a2params))+0.1)
#plt.xlim(0, x[-1])
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$U / \si{\volt}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'a1')


#   a2
x = np.linspace(unp.nominal_values(a2Koordinaten)[0][0],unp.nominal_values(a2Koordinaten)[0][-1])
plt.cla()
plt.clf()
plt.plot(*unp.nominal_values(a2Koordinaten), 'rx', label='a2')
plt.plot(x, line(x, *unp.nominal_values(a2params)), 'b-', label='a2fit')
#plt.ylim(0, line(x[-1], *unp.nominal_values(a2params))+0.1)
#plt.xlim(0, x[-1])
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$U / \si{\volt}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'a2')

#   c
x = np.linspace(unp.nominal_values(cKoordinaten)[0][0],unp.nominal_values(cKoordinaten)[0][-1])
plt.cla()
plt.clf()
plt.plot(*unp.nominal_values(cKoordinaten), 'rx', label='c')
plt.plot(x, line(x, *unp.nominal_values(cparams)), 'b-', label='cfit')
#plt.ylim(0, line(x[-1], *unp.nominal_values(a2params))+0.1)
#plt.xlim(0, x[-1])
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$U / \si{\volt}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'c')
