from table import makeTable
from table import makeNewTable
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


#makeTable([Array mit den einzelnen Datenarrays], r'{'+r'Überschrift'+r'} & ' ,'tabges' , ['S[table-format=2.0]', ] ,  ["%2.0f", ])

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


#1. Messwerte einlesen
winkel = np.array([60,15,-30])
dopplerwinkel = 90-180/np.pi*(np.arcsin(np.sin(winkel*2*(np.pi)/360)*1800/2700))
print("dopplerwinkel",dopplerwinkel)
kleinrohr = np.array(np.genfromtxt('scripts/klein', unpack=True))
mittelrohr = np.array(np.genfromtxt('scripts/mittel', unpack = True))
grossrohr = np.array(np.genfromtxt('scripts/gross', unpack=True))#leistung,45,60,30
tiefm45 = np.array(np.genfromtxt('scripts/tiefenmessung45', unpack=True))
tiefm70 = np.array(np.genfromtxt('scripts/tiefenmessung70', unpack=True))
messtiefe = np.array(np.linspace(30,41,16))
intens = np.array([tiefm45[2],tiefm70[2]])

def vFluss(deltaf, dopplerwinkel):
    return deltaf*1800/(2*2*10**6*np.cos(dopplerwinkel*2*np.pi/360))

def linfit(a,x,b):
    return a*x+b

Vkleinrohr = np.array([vFluss(kleinrohr[1],dopplerwinkel[0]),vFluss(kleinrohr[2],dopplerwinkel[1]),vFluss(kleinrohr[3],dopplerwinkel[2])])
print("Vkleinrohr",Vkleinrohr)
Vmittelrohr = np.array([vFluss(mittelrohr[1],dopplerwinkel[0]),vFluss(mittelrohr[2],dopplerwinkel[1]),vFluss(mittelrohr[3],dopplerwinkel[2])])
print("Vmittelrohr",Vmittelrohr)
Vgrossrohr = np.array([vFluss(grossrohr[1],dopplerwinkel[0]),vFluss(grossrohr[2],dopplerwinkel[1]),vFluss(grossrohr[3],dopplerwinkel[2])])
print("Vgrossrohr",Vgrossrohr)

#Graphen erstellen:
#Vkleinrohr
i=0
while i<3:
    lin = curve_fit(linfit,Vkleinrohr[i]*100,kleinrohr[i+1]/np.cos(dopplerwinkel[i]*2*np.pi/360))
    linfits = [lin[0],np.sqrt(np.diag(lin[1]))]
    print("lineare Fits Daten von"+str(winkel[i])+":",linfits)
    plt.cla()
    plt.clf()
    punkte = np.linspace(0,Vkleinrohr[i][-1]*1.1*100,1000)
    plt.plot(Vkleinrohr[i]*100, kleinrohr[i+1]/np.cos(dopplerwinkel[i]*2*np.pi/360),'gx', label='kleines Rohr und '+str(winkel[i])+' grad')
    plt.plot(punkte,linfit(linfits[0][0],punkte,linfits[0][1]),label = 'linearer Fit')
#plt.plot(Vkleinrohr[1]*100, kleinrohr[2]/np.cos(dopplerwinkel[1]),'rx', label='kleines rohr und 15(60) grad')

#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(0, t[-1]*100)
    plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
    plt.ylabel(r'$V/cos(alpha)$')
    plt.legend(loc='best')
    plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
    plt.savefig('build/'+'deltacosperV'+str(winkel[i]))
    i = i+1
print("lineareFits",linfits)
#Tiefenmessungen,doppler60
messtiefen = np.array(tiefm45[0])
Vtiefen = np.array([vFluss(tiefm45[1],dopplerwinkel[0]),vFluss(tiefm70[1],dopplerwinkel[0])])
print("Vtiefen:",Vtiefen)
P = np.array([45,70])
i=0
while i<2:
    plt.cla()
    plt.clf()
    plt.plot(messtiefen, Vtiefen[i]*100,'gx', label='die Momentangeschwindigkeit bei einer Leistung von '+str(P[i])+'%')
    plt.plot(messtiefen, intens[i]/100,'rx', label='die Streuintensität bei einer Leistung von '+str(P[i])+'%')
#plt.plot(Vkleinrohr[1]*100, kleinrohr[2]/np.cos(dopplerwinkel[1]),'rx', label='kleines rohr und 15(60) grad')

#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(0, t[-1]*100)
    plt.xlabel(r'$z/\si{\milli\meter}$')
    plt.ylabel(r'$v_\text{m}/\si{\centi\meter\per\second}$')
    plt.legend(loc='best')
    plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
    plt.savefig('build/'+'messtiefe'+str(P[i]))
    i = i+1
