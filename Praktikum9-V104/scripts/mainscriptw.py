from table import makeTable
from bereich import bereich
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp

# ALLES---------------------------------------------------------------------------------


def betrag(x):
    return unp.sqrt(x**2)

vNull = 16594
vNull *= 5/4
print('vNull:', vNull)
# Vmessung------------------------------------------------------------------------------
Gang, timeForwards, timeBackwards = np.genfromtxt('scripts/Vmessung', unpack=True)
makeTable([Gang[0:int(len(Gang)/2)], timeForwards[0:int(len(Gang)/2)], timeBackwards[0:int(len(Gang)/2)]], r'{ Gang } & {$ t_\text{v}/\si{\milli\second} $} & { $ t_\text{r}/\si{\milli\second} $ }', 'tabv1', [r'S[table-format=2.0]', r'S[table-format=4.0]', r'S[table-format=4.0]'], ["%2.0f", "%4.0f", "%4.0f"])
makeTable([Gang[int(len(Gang)/2):], timeForwards[int(len(Gang)/2):], timeBackwards[int(len(Gang)/2):]], r'{ Gang } & {$ t_\text{v}/\si{\milli\second} $} & { $ t_\text{r}/\si{\milli\second} $ }', 'tabv2', [r'S[table-format=2.0]', r'S[table-format=4.0]', r'S[table-format=4.0]'], ["%2.0f", "%4.0f", "%4.0f"])
LaengeDerStrecke = 445

ForwardsV = []
for i in range(1, 11):
    ForwardsV.append(LaengeDerStrecke / unp.uarray(np.mean(timeForwards[Gang == i*6]), stats.sem(timeForwards[Gang == i*6])))
ForwardsV = np.array(ForwardsV)

BackwardsV = []
for i in range(1, 11):
    BackwardsV.append(-LaengeDerStrecke / unp.uarray(np.mean(timeBackwards[Gang == i*6]), stats.sem(timeBackwards[Gang == i*6])))
BackwardsV = np.array(BackwardsV)

print(ForwardsV)
print(BackwardsV)



# Dopplereffektmessung------------------------------------------------------------------

Gang, frequenzForwards, frequenzBackwards = np.genfromtxt('scripts/dopllereffektmessung', unpack=True)
frequenzForwards *= 5/4
frequenzBackwards *= 5/4
frequenzForwards[Gang==6] = frequenzForwards[Gang==6]/10
frequenzBackwards[Gang==6] = frequenzBackwards[Gang==6]/10
makeTable([Gang[0:int(len(Gang)/2)], frequenzForwards[0:int(len(Gang)/2)], frequenzBackwards[0:int(len(Gang)/2)]], r'{'+r'Gang'+r'} & {'+r'$f_\text{v}/\si{\hertz}$'+r'} & {'+r'$f_\text{r}/\si{\hertz}$'+r'}', 'tab1', ['S[table-format=2.0]', 'S[table-format=5.0]', 'S[table-format=5.0]'], ["%2.0f", "%5.0f", "%5.0f"])
makeTable([Gang[int(len(Gang)/2):], frequenzForwards[int(len(Gang)/2):], frequenzBackwards[int(len(Gang)/2):]], r'{'+r'Gang'+r'} & {'+r'$f_\text{v}/\si{\hertz}$'+r'} & {'+r'$f_\text{r}/\si{\hertz}$'+r'}', 'tab2', ['S[table-format=2.0]', 'S[table-format=5.0]', 'S[table-format=5.0]'], ["%2.0f", "%5.0f", "%5.0f"])


Forwards = []
for i in range(1, 11):
	Forwards.append(unp.uarray(np.mean(frequenzForwards[Gang==i*6]), stats.sem(frequenzForwards[Gang==i*6])))
Forwards = np.array(Forwards)

Backwards = []
for i in range(1, 11):
	Backwards.append(unp.uarray(np.mean(frequenzBackwards[Gang==i*6]), stats.sem(frequenzBackwards[Gang==i*6])))
Backwards = np.array(Backwards)

print(Forwards)
print(Backwards)

# DeltaVKursiv--------------------------------------------------------------------------
DeltaVForwards = []
for value in Forwards:
    DeltaVForwards.append(value-vNull)
DeltaVForwards = np.array(DeltaVForwards)

DeltaVBackwards = []
for value in Backwards:
    DeltaVBackwards.append(value-vNull)
DeltaVBackwards = np.array(DeltaVBackwards)

print(DeltaVForwards)
print(DeltaVBackwards)

# PlotVonDeltaVKursivGegenV-------------------------------------------------------------
ForwardsVNominal = []
ForwardsVStd = []
for value in ForwardsV:
    ForwardsVNominal.append(unp.nominal_values(value))
    ForwardsVStd.append(unp.std_devs(value))
ForwardsVNominal = np.array(ForwardsVNominal)
ForwardsVStd = np.array(ForwardsVStd)

BackwardsVNominal = []
BackwardsVStd = []
for value in BackwardsV:
    BackwardsVNominal.append(unp.nominal_values(value))
    BackwardsVStd.append(unp.std_devs(value))
BackwardsVNominal = np.array(BackwardsVNominal)
BackwardsVStd = np.array(BackwardsVStd)

Gaenge = np.array([6,12,18,24,30,36,42,48,54,60])
makeTable([Gaenge, ForwardsVNominal*100, ForwardsVStd*100, BackwardsVNominal*100, BackwardsVStd*100], r'{'+r'Gang'+r'} & \multicolumn{2}{c}{'+r'$v_\text{v}/\si[per-mode=reciprocal]{\centi\meter\per\second}$'+r'} & \multicolumn{2}{c}{'+r'$v_\text{r}/\si[per-mode=reciprocal]{\centi\meter\per\second}$'+r'}', 'tabges', ['S[table-format=2.0]', 'S[table-format=2.3]', ' @{${}\pm{}$} S[table-format=1.3]', 'S[table-format=3.3]', ' @{${}\pm{}$} S[table-format=1.3]'], ["%2.0f", "%2.3f", "%2.3f", "%2.3f", "%2.3f"])


VNominal = np.append(BackwardsVNominal, ForwardsVNominal)


DeltaVForwardsNominal = []
DeltaVForwardsStd = []
for value in DeltaVForwards:
    DeltaVForwardsNominal.append(unp.nominal_values(value))
    DeltaVForwardsStd.append(unp.std_devs(value))
DeltaVForwardsNominal = np.array(DeltaVForwardsNominal)
DeltaVForwardsStd = np.array(DeltaVForwardsStd)

DeltaVBackwardsNominal = []
DeltaVBackwardsStd = []
for value in DeltaVBackwards:
    DeltaVBackwardsNominal.append(unp.nominal_values(value))
    DeltaVBackwardsStd.append(unp.std_devs(value))
DeltaVBackwardsNominal = np.array(DeltaVBackwardsNominal)
DeltaVBackwardsStd = np.array(DeltaVBackwardsStd)

DeltaVNominal = np.append(DeltaVBackwardsNominal, DeltaVForwardsNominal)



def line(x, a):
    return a*x


params, covar = curve_fit(line, VNominal, DeltaVNominal, maxfev=1000)
print(params, covar, sep='\n')

t = np.linspace(-ForwardsVNominal[-1]*1.03, ForwardsVNominal[-1]*1.03, 1000)
plt.cla()
plt.clf()
plt.plot(t*100, line(t, *params), 'b-', label='Fit')
plt.plot(ForwardsVNominal*100, DeltaVForwardsNominal, 'gx', label='Daten mit Bewegungsrichtung aufs Mikrofon zu')
plt.plot(BackwardsVNominal*100, DeltaVBackwardsNominal, 'r+', label='Daten mit Bewegungsrichtung vom Mikrofon weg')
#plt.ylim(-line(t[-1], line(t[-1], *params)+0.1)
plt.xlim(-t[-1]*100, t[-1]*100)
plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
plt.ylabel(r'$\Delta f / \si{\hertz}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'VgegenDeltaV')

a = unp.uarray(params[0], np.sqrt(covar[0][0]))
print('vNull/c:', a)
print('c:', vNull/a)

# makeTable([x[0:int(len(x)/2)]*100, yd[0:int(len(yd)/2)]*1000], r'{'+namex+r'} & {'+namey+r'}', 'tabbeidseitig1', ['S[table-format=2.1]', 'S[table-format=1.2]'], ["%3.1f", "%3.2f"])


# a = unp.uarray(params[0], np.sqrt(covar[0][0]))

# Schallges-----------------------------------------------------------------------------

x, y = np.genfromtxt('scripts/Wellenlängenmessungundnormalfrequenz', unpack=True)
print(y)
makeTable([y], r'{'+r'$x/\si{\milli\meter}$'+r'}', 'tabwelle', [r'S[table-format=2.2]'], ["%2.2f"])
y = y - y[0]
wellenlaenge = unp.uarray(np.mean(y[1:]/x[1:]), stats.sem(y[1:]/x[1:]))
print('Wellenlänge:', wellenlaenge, 'mm')
print('1/Wellenlänge:', (1/wellenlaenge), '1/mm')
print('c:', wellenlaenge*vNull/1000, 'm/s')

# t-Test--------------------------------------------------------------------------------

a1 = 1/wellenlaenge *1000
n = len(y) - 1
a1m = unp.nominal_values(a1)
sx = unp.std_devs(a1)
a2 = a
m = len(DeltaVNominal)
a2m = unp.nominal_values(a2)
sy = unp.std_devs(a2)
s = np.sqrt(((n-1)*sx**2+(m-1)*sy**2)/(n+m-2))
print('n', n)
print('m', m)
print('Anzahl der Freiheitsgerade (n+m-2)', m+n-2)
print('s', s)
t = np.sqrt((n*m)/(n+m))* (a1m-a2m)/s
print('t', t)
print('Nach dem t-Test nahezu 100 Prozent Wahrscheinlichkeit einer systematischen Abweichung')
