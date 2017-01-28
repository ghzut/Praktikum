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

# Messing Schmal 9 x 0.7 x 0.4 93+-12
AMessingS = 0.007*0.004
pMessingS = 8520
cMessingS = 385
kMessingS = 93
print('p*c MessingS:',pMessingS*cMessingS)

# Messing Breit 9 x 1.2 x 0.4
AMessingB = 0.012*0.004
pMessingB = 8520
cMessingB = 385
kMessingB = 93
print('p*c MessingB:',pMessingB*cMessingB)

# Aluminium 9 x 1.2 x 0.4
AAluminium = 0.012*0.004
pAluminium = 2800
cAluminium = 830
kAluminium = 220
print('p*c Aluminium:',pAluminium*cAluminium)

# Edelstahl 9 x 1.2 x 0.4
AEdlestahl = 0.012*0.004
pEdelstahl = 8000
cEdlestahl = 400
kEdelstahl = 20
print('p*c Edelstahl:',pEdelstahl*cEdlestahl)

# Abstand zwischen Thermoelementen an einem Stab
AbT = 0.03

# Hauptscript

x21, dT21 = np.genfromtxt("scripts/T2-T1", unpack=True)
x78, dT78 = np.genfromtxt("scripts/T7-T8", unpack=True)
x21, x78 = x21*1000/7.55, x78*1000/7.55
dT21, dT78 = dT21*2.5/11.7, dT78*5/8.9
def line(x, a, b):
    return a*x+b

# Die zeitlichen Abstände berechnen (unnötig)
dx21 = []
dx21.append(x21[0])
for i in range(len(x21)-1):
    dx21.append(x21[i+1]-x21[i])
dx21 = np.array(dx21)
dx78 = []
dx78.append(x78[0])
for i in range(len(x78)-1):
    dx78.append(x78[i+1]-x78[i])
dx78 = np.array(dx78)

# Den Wärmestrom berechnen und ausgeben und Tabelle erstellen
print('dT21/AbT:')
print(dT21/AbT)
print('dT78/AbT:')
print(dT78/AbT)
print('Wärmefluss T21')
print(-dT21/AbT * AMessingB *kMessingB)
print('Wärmefluss T78')
print(-dT78/AbT * AEdlestahl *kEdelstahl)

makeTable([x21, dT21, -dT21/AbT * AMessingB *kMessingB], r'{$t/\si{\second}$} & {$(T2-T1)/\si{\kelvin}$} & {$\frac{\Delta Q_\text{21}}{\Delta t}/\si{\watt}$}', 'tabT21', [r'S[table-format=4.0]', r'S[table-format=1.1]', r'S[table-format=1.3]'], ["%4.0f", "%1.1f", "%0.3f"])
makeTable([x78, dT78, -dT78/AbT * AEdlestahl *kEdelstahl], r'{$t/\si{\second}$} & {$(T7-T8)/\si{\kelvin}$} & {$\frac{\Delta Q_\text{78}}{\Delta t}/\si{\watt}$}', 'tabT78', [r'S[table-format=4.0]', r'S[table-format=1.1]', r'S[table-format=1.3]'], ["%4.0f", "%1.1f", "%0.3f"])

# Berechnung von den kappas

def kappa(Anah, Afern, deltat, p, c):
	return (p*c*0.03**2) / (2*deltat*unp.log(Anah/Afern))

AnahMessing, AfernMessing, deltatMessing = np.genfromtxt('scripts/Messing', unpack=True)
AnahMessing *= 10/5.8 /2
AfernMessing *= 10/5.8 /2
deltatMessing *= 1000/14.95
AnahAluminium, AfernAluminium, deltatAluminium = np.genfromtxt('scripts/Aluminium', unpack=True)
AnahAluminium *= 10/5.8 /2
AfernAluminium *= 10/5.8 /2
deltatAluminium *= 1000/14.95
AnahEdelstahl, AfernEdelstahl, deltatEdelstahl = np.genfromtxt('scripts/Edelstahl', unpack=True)
AnahEdelstahl *= 100/23
AfernEdelstahl *= 100/23
deltatEdelstahl *= 1000/11.9

makeTable([AnahMessing, AfernMessing, deltatMessing], r'{$A_\text{nah}$} & {$A_\text{fern}$} & {$\Delta t / \si{\second}$}', 'tabMessing', [r'S[table-format=1.2]', r'S[table-format=1.2]', r'S[table-format=2.0]'], ["%1.2f", "%1.2f", "%2.0f"])
makeTable([AnahAluminium, AfernAluminium, deltatAluminium], r'{$A_\text{nah}$} & {$A_\text{fern}$} & {$\Delta t / \si{\second}$}', 'tabAluminium', [r'S[table-format=1.1]', r'S[table-format=1.1]', r'S[table-format=1.1]'], ["%1.1f", "%1.1f", "%1.1f"])
makeTable([AnahEdelstahl, AfernEdelstahl, deltatEdelstahl], r'{$A_\text{nah}$} & {$A_\text{fern}$} & {$\Delta t / \si{\second}$}', 'tabEdelstahl', [r'S[table-format=1.1]', r'S[table-format=1.1]', r'S[table-format=2.0]'], ["%1.1f", "%1.1f", "%2.0f"])


# Mittelwert + Standartabweichung des Mittelwertes Messing
AnahMessing = unp.uarray(np.mean(AnahMessing), stats.sem(AnahMessing))
print('AnahMessing:', AnahMessing)
AfernMessing = unp.uarray(np.mean(AfernMessing), stats.sem(AfernMessing))
print('AfernMessing:', AfernMessing)
deltatMessing = unp.uarray(np.mean(deltatMessing), stats.sem(deltatMessing))
print('deltatMessing:', deltatMessing)
print('KappaMessing:', kappa(AnahMessing, AfernMessing, deltatMessing, pMessingB, cMessingB))

# Mittelwert + Standartabweichung des Mittelwertes Aluminium
AnahAluminium = unp.uarray(np.mean(AnahAluminium), stats.sem(AnahAluminium))
print('AnahAluminium:', AnahAluminium)
AfernAluminium = unp.uarray(np.mean(AfernAluminium), stats.sem(AfernAluminium))
print('AfernAluminium:', AfernAluminium)
deltatAluminium = unp.uarray(np.mean(deltatAluminium), stats.sem(deltatAluminium))
print('deltatAluminium:', deltatAluminium)
print('KappaAluminium:', kappa(AnahAluminium, AfernAluminium, deltatAluminium, pAluminium, cAluminium))

# Mittelwert + Standartabweichung des Mittelwertes Edelstahl
AnahEdelstahl = unp.uarray(np.mean(AnahEdelstahl), stats.sem(AnahEdelstahl))
print('AnahEdelstahl:', AnahEdelstahl)
AfernEdelstahl = unp.uarray(np.mean(AfernEdelstahl), stats.sem(AfernEdelstahl))
print('AfernEdelstahl:', AfernEdelstahl)
deltatEdelstahl = unp.uarray(np.mean(deltatEdelstahl), stats.sem(deltatEdelstahl))
print('deltatEdelstahl:', deltatEdelstahl)
print('KappaEdelstahl:', kappa(AnahEdelstahl, AfernEdelstahl, deltatEdelstahl, pEdelstahl, cEdlestahl))
