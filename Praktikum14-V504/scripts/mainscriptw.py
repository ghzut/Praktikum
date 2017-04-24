from table import makeTable
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

# Messwerte

#Der erste Versuch 8a:
V1wo2_5 = np.genfromtxt('scripts/DatenV1', unpack=True)
print(V1wo2_5)
print("Die letzte Durchführung bei 2.5A")
V1ol2_5 = np.genfromtxt("scripts/DatenV1_2.5",unpack=True)
print(V1ol2_5)
#Der zweite Versuch 8c:
print("Der zweite Versuch")
V2 = np.genfromtxt("scripts/DatenV2",unpack=True)
print(V2)
V3=V2


#8a:
plt.plot(V1wo2_5[0], V1wo2_5[1], 'g+', label='I = 2,0 A')
plt.plot(V1wo2_5[0], V1wo2_5[2], 'go', label='I = 2,1 A')
plt.plot(V1wo2_5[0], V1wo2_5[3], 'r+', label='I = 2,2 A')
plt.plot(V1wo2_5[0], V1wo2_5[4], 'ro', label='I = 2,3 A')
plt.plot(V1wo2_5[0], V1wo2_5[5], 'bo', label='I = 2,4 A')
plt.plot(V1ol2_5[0], V1ol2_5[1], 'yo', label='I = 2,5 A')
#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(0, t[-1]*100)
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$I / \si{\micro\ampere}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'Kennlinien')
plt.cla()
plt.clf()


print("yeah")
logV1 = [[np.log(x) for x in V1ol2_5[0]],[np.log(x*10**-6) for x in V1ol2_5[1]]]
print(logV1)
#intressanterBereich
x42 = np.linspace(logV1[0][1],logV1[0][-2],1000)
def linfunc(x,a,b):
    return a*x+b
#m = logV2[0][6]
#vermuteter Gültigkeitsbereich
lin = curve_fit(linfunc,logV1[0][6:18],logV1[1][6:18])
print(lin)
linspast=lin
lin = [lin[0],np.sqrt(np.diag(lin[1]))]
lin = unp.uarray(lin[0],lin[1])
print(x42)


#richtige göße gefixt ^^
#doppeltlogarithmischI=2.5
plt.plot(logV1[0], logV1[1], 'yx', label ="logarithmische Darstellung der höchsten Kennlinie")
plt.plot(x42,x42*linspast[0][0]+linspast[0][1],label = "gefittete Ausgleichsgerade")
#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(0, t[-1]*100)
plt.xlabel(r'$\log (U/\si{\volt})$')
plt.ylabel(r'$\log (I/\si{\ampere})$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'Kennlinielog')
plt.cla()
plt.clf()

#8c:
V2 = np.array([V2[0]+V2[1]*0.001,V2[1]*10**(-9)])
print(V2)


print("yeah")
logV2 = [V2[0],np.log(V2[1])]
print(logV2)



linV2 = curve_fit(linfunc,logV2[0],logV2[1])
linV3 = linV2
print("hi")
linV2 = [linV2[0],np.sqrt(np.diag(linV2[1]))]
linV2 = unp.uarray(linV2[0],linV2[1])
print(linV2)
Heiztemp = - const.value("electron volt")/(linV2[0]*const.value("Boltzmann constant"))
print ("Stevae")
print(Heiztemp)
print ("Stevae")

x2 = np.linspace(logV2[0][0],logV2[0][-1],1000)

#einfachlogarithmischI=2.5
plt.plot(logV2[0], logV2[1], 'yx', label ="halblogarithmische Darstellung des Anlaufstromgebietes")
plt.plot(x2,linV3[0][0]*x2+linV3[0][1],label = "gefittete Ausgleichsgerade")
#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(0, t[-1]*100)
plt.xlabel(r'$U/\si{\volt}$')
plt.ylabel(r'$\log (I / \si{\ampere})$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'KennlinielogV2')
plt.cla()
plt.clf()

#8d:
andereAngabenU = np.linspace(4.0,5.75,6)
andereAngabenI = [2.0,2.1,2.2,2.3,2.4,2.5]
andereAngabenW = andereAngabenI*andereAngabenU
andereAngabenW = andereAngabenW - 1
andereheiztemp = andereAngabenW/(5.7*10**(-12)*0.32*0.28)
andereheiztemp = andereheiztemp**(0.25)
print(andereheiztemp)
#8e:
Heiztemp = np.array(andereheiztemp[0:-1])
letzterkram = np.array([V1wo2_5[1][25],V1wo2_5[2][25],V1wo2_5[3][25],1500,3000])
meh = (const.value("Planck constant")/const.value("Boltzmann constant"))*(const.value("Planck constant")/const.value("Boltzmann constant"))*(const.value("Planck constant")/const.value("electron volt"))/(0.000032*const.value("electron mass"))
print("meh")
print(meh)
letz = -np.log(meh*letzterkram/(4*np.pi*(Heiztemp**2)))
print(letz)
letz = letz *const.value("Boltzmann constant")*Heiztemp/const.value("electron volt")
print(letzterkram)
print(letz)
tdletz = np.mean(letz)
stderrletz = stats.sem(letz)
print("nochmehrkram")
print(tdletz)
print(stderrletz)
#1. Datentabelle
makeTable([V1wo2_5[0],V1wo2_5[1],V1wo2_5[2],V1wo2_5[3],V1wo2_5[4]], r'{'+r'$U/\si{\volt}$'+r'} & {'+r'$I_\text{2,1}/\si{\micro\ampere}$'+r'} & {'+r'$I_\text{2,2}/\si{\micro\ampere}$'+r'} & {'+r'$I_\text{2,3}/\si{\micro\ampere}$'+r'} & {'+r'$I_\text{2,4}/\si{\micro\ampere}$'+r'}' ,'tabV1wo' , ['S[table-format=4.0]' , 'S[table-format=4.0]' , 'S[table-format=4.0]' , 'S[table-format=4.0]' , 'S[table-format=4.0]'] , ["%4.0f", "%4.0f","%4.0f","%4.0f","%4.0f"])

#2.datentabelle
makeTable([V1ol2_5[0] [0:len(V1ol2_5[0])//2],V1ol2_5[1] [0:len(V1ol2_5[0])//2] ], r'{'+r'$U/\si{\volt}$'+r'} & {'+r'$I_\text{2,5}/\si{\micro\ampere}$'+r'}' ,'tabV1ol1' , ['S[table-format=3.0]' , 'S[table-format=4.0]'] ,  ["%3.0f", "%4.0f"])

makeTable([V1ol2_5[0][(len(V1ol2_5[0]))//2+1:(len(V1ol2_5[0]))] ,V1ol2_5[0][(len(V1ol2_5[0]))//2+1:(len(V1ol2_5[0]))]] , r'{'+r'$U/\si{\volt}$'+r'} & {'+r'$I_\text{2,5}/\si{\micro\ampere}$'+r'}' ,'tabV1ol2' , ['S[table-format=3.0]' , 'S[table-format=4.0]'] ,  ["%3.0f", "%4.0f"])

#3.datentabelle
makeTable([V3[0],V3[1]], r'{'+r'$U/\si{\volt}$'+r'} & {'+r'$I/\si{\nano\ampere}$'+r'}' ,'tabV2' , ['S[table-format=1.2]' , 'S[table-format=2.2]'] ,  ["%1.2f", "%2.2f"])

makeTable([andereAngabenI[0:5],andereAngabenW[0:5],letzterkram], r'{'+r'$I_\text{f}/\si{\ampere}$'+r'} & {'+r'$W_\text{f}/\si{\watt}$'+r'} &{'+r'$I_\text{S}/\si{\micro\ampere}$'+r'}' ,'IS' , ['S[table-format=3.1]', 'S[table-format=3.1]' , 'S[table-format=4.0]'] ,  ["%3.1f","%3.1f", "%4.0f"])

makeTable([andereAngabenI[0:5],andereAngabenW[0:5],andereheiztemp], r'{'+r'$I_\text{f}/\si{\ampere}$'+r'} & {'+r'$W_\text{f}/\si{\watt}$'+r'} &{'+r'$T_\text{S}$'+r'}' ,'tabheiz' , ['S[table-format=3.1]', 'S[table-format=3.2]' , 'S[table-format=4.0]'] ,  ["%3.1f","%3.2f", "%4.0f"])
