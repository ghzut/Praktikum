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
#messtiefe = np.array(np.linspace(30,41,16))
intens = np.array([tiefm45[2],tiefm70[2]])
rohrdurchmesser = np.array([0.007,0.010,0.016])

def vFlussP(d,P):
    return P/100*0.01/((d/2)**2*np.pi)/60

def vFluss(deltaf, dopplerwinkel):
    return deltaf*1800/(2*2*10**6*np.cos(dopplerwinkel*2*np.pi/360))

def linfit(a,x,b):
    return a*x+b
#dopplerv
Vkleinrohr = np.array([vFluss(kleinrohr[1],dopplerwinkel[0]),vFluss(kleinrohr[2],dopplerwinkel[1]),vFluss(kleinrohr[3],dopplerwinkel[2])])
print("Vkleinrohr",Vkleinrohr)
Vmittelrohr = np.array([vFluss(mittelrohr[1],dopplerwinkel[0]),vFluss(mittelrohr[2],dopplerwinkel[1]),vFluss(mittelrohr[3],dopplerwinkel[2])])
print("Vmittelrohr",Vmittelrohr)
Vgrossrohr = np.array([vFluss(grossrohr[1],dopplerwinkel[0]),vFluss(grossrohr[2],dopplerwinkel[1]),vFluss(grossrohr[3],dopplerwinkel[2])])
print("Vgrossrohr",Vgrossrohr)
#leistungv
VkleinrohrP = np.array(vFlussP(rohrdurchmesser[0],kleinrohr[0]))
print("VkleinrohrP",Vkleinrohr)
VmittelrohrP = np.array(vFlussP(rohrdurchmesser[1],mittelrohr[0]))
print("VmittelrohrP",Vmittelrohr)
VgrossrohrP = np.array(vFlussP(rohrdurchmesser[2],grossrohr[0]))
print("VgrossrohrP",Vgrossrohr)

steigung = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
fehler = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
#Graphen erstellen:
#Vkleinrohr
j=0
i=0
while i<3:
    lin = curve_fit(linfit,VkleinrohrP*100,kleinrohr[i+1]/np.cos(dopplerwinkel[i]*2*np.pi/360))
    linfits = [lin[0],np.sqrt(np.diag(lin[1]))]
    print("lineare Fits Daten von"+str(winkel[i])+":",linfits)
    steigung[j] = linfits[0][0]
    fehler[j] = linfits[1][0]
    plt.cla()
    plt.clf()
    punkte = np.linspace(0,VkleinrohrP[-1]*1.1*100,1000)
    plt.plot(VkleinrohrP*100, kleinrohr[i+1]/np.cos(dopplerwinkel[i]*2*np.pi/360),'gx', label='kleines Rohr und '+str(winkel[i])+r'$\si{\degree}$')
    plt.plot(punkte,linfit(linfits[0][0],punkte,linfits[0][1]),label = 'linearer Fit')
    plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
    plt.ylabel(r'$V/cos(\alpha)$')
    plt.legend(loc='best')
    plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
    plt.savefig('build/'+'deltacosperV'+str(winkel[i]))
    i = i+1
    j = j+1
#Vmittelrohr
i=0
while i<3:
    lin = curve_fit(linfit,VmittelrohrP*100,mittelrohr[i+1]/np.cos(dopplerwinkel[i]*2*np.pi/360))
    linfits = [lin[0],np.sqrt(np.diag(lin[1]))]
    print("lineare Fits Daten von"+str(winkel[i])+":",linfits)
    steigung[j] = linfits[0][0]
    fehler[j] = linfits[1][0]
    plt.cla()
    plt.clf()
    punkte = np.linspace(0,VmittelrohrP[-1]*1.1*100,1000)
    plt.plot(VmittelrohrP*100, mittelrohr[i+1]/np.cos(dopplerwinkel[i]*2*np.pi/360),'gx', label='mittleres Rohr und '+str(winkel[i])+r'$\si{\degree}$')
    plt.plot(punkte,linfit(linfits[0][0],punkte,linfits[0][1]),label = 'linearer Fit')
    plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
    plt.ylabel(r'$V/cos(\alpha)$')
    plt.legend(loc='best')
    plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
    plt.savefig('build/'+'deltacosperVmittel'+str(winkel[i]))
    i = i+1
    j = j+1
i=0
while i<3:
    lin = curve_fit(linfit,VgrossrohrP*100,grossrohr[i+1]/np.cos(dopplerwinkel[i]*2*np.pi/360))
    linfits = [lin[0],np.sqrt(np.diag(lin[1]))]
    print("lineare Fits Daten von"+str(winkel[i])+":",linfits)
    steigung[j] = linfits[0][0]
    fehler[j] = linfits[1][0]
    plt.cla()
    plt.clf()
    punkte = np.linspace(0,VgrossrohrP[-1]*1.1*100,1000)
    plt.plot(VgrossrohrP*100, grossrohr[i+1]/np.cos(dopplerwinkel[i]*2*np.pi/360),'gx', label='großes Rohr und '+str(winkel[i])+r'$\si{\degree}$')
    plt.plot(punkte,linfit(linfits[0][0],punkte,linfits[0][1]),label = 'linearer Fit')
    plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
    plt.ylabel(r'$V/cos(\alpha)$')
    plt.legend(loc='best')
    plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
    plt.savefig('build/'+'deltacosperVgross'+str(winkel[i]))
    i = i+1
    j = j+1

Steigungen = unp.uarray(steigung,fehler)
print("lineareFits",Steigungen)
Steigungm = unp.uarray(np.mean(unp.nominal_values(Steigungen)), stats.sem(unp.nominal_values(Steigungen)))
print("steigungm:",Steigungm)

#Tiefenmessungen,doppler60
messtiefen = np.array(tiefm45[0])
Vtiefen = np.array([vFluss(tiefm45[1],dopplerwinkel[1]),vFluss(tiefm70[1],dopplerwinkel[1])])
print("Vtiefen:",Vtiefen)
P = np.array([45,70])
i=0
while i<2:
    plt.cla()
    plt.clf()
    plt.plot(messtiefen, Vtiefen[i]*100,'gx', label=r'$v_\text{mom}$ mit $P$ = '+str(P[i])+'%')
    plt.plot(messtiefen, intens[i]/125,'rx', label=r'$\SI{0.8}{\percent}$ von $I_\text{Streu}$ mit $P$ = '+str(P[i])+'%')
#plt.plot(Vkleinrohr[1]*100, kleinrohr[2]/np.cos(dopplerwinkel[1]),'rx', label='kleines rohr und 15(60) grad')
#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(0, t[-1]*100)
    plt.xlabel(r'$z/\si{\milli\meter}$')
    plt.ylabel(r'$v_\text{m}/\si{\centi\meter\per\second}$')
    plt.legend(loc='best')
    plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
    plt.savefig('build/'+'messtiefe'+str(P[i]))
    i = i+1


#tabellen:daten
makeTable([kleinrohr[0],kleinrohr[1],kleinrohr[2],kleinrohr[3],VkleinrohrP*100], r'{'+r'$P/\si{\percent}$'+r'} & {'+r'$\Delta f_{\text{Winkel:}\SI{60}{\degree}}$'+r'} & {'+r'$\Delta f_{\text{Winkel:}\SI{15}{\degree}}$'+r'} & {'+r'$\Delta f_{\text{Winkel:}\SI{-30}{\degree}}$'+r'} & {'+r'$v/\si[per-mode=reciprocal]{\centi\meter\per\second}$'+r'}' ,'tabkleinrohr' , ['S[table-format=2.1]' , 'S[table-format=4.0]', 'S[table-format=4.0]', 'S[table-format=4.0]', 'S[table-format=3.0]'] ,  ["%1.2f", "%4.0f", "%4.0f", "%4.0f", "%3.0f"])
makeTable([mittelrohr[0],mittelrohr[1],mittelrohr[2],mittelrohr[3],VmittelrohrP*100], r'{'+r'$P/\si{\percent}$'+r'} & {'+r'$\Delta f_{\text{Winkel:}\SI{60}{\degree}}$'+r'} & {'+r'$\Delta f_{\text{Winkel:}\SI{15}{\degree}}$'+r'} & {'+r'$\Delta f_{\text{Winkel:}\SI{-30}{\degree}}$'+r'} & {'+r'$v/\si[per-mode=reciprocal]{\centi\meter\per\second}$'+r'}' ,'tabmittelrohr' , ['S[table-format=2.1]' , 'S[table-format=4.0]', 'S[table-format=4.0]', 'S[table-format=4.0]', 'S[table-format=3.0]'] ,  ["%1.2f", "%4.0f", "%4.0f", "%4.0f", "%3.0f"])
makeTable([grossrohr[0],grossrohr[1],grossrohr[2],grossrohr[3],VgrossrohrP*100], r'{'+r'$P/\si{\percent}$'+r'} & {'+r'$\Delta f_{\text{Winkel:}\SI{60}{\degree}}$'+r'} & {'+r'$\Delta f_{\text{Winkel:}\SI{15}{\degree}}$'+r'} & {'+r'$\Delta f_{\text{Winkel:}\SI{-30}{\degree}}$'+r'} & {'+r'$v/\si[per-mode=reciprocal]{\centi\meter\per\second}$'+r'}' ,'tabgrossrohr' , ['S[table-format=2.1]' , 'S[table-format=4.0]', 'S[table-format=4.0]', 'S[table-format=4.0]', 'S[table-format=3.0]'] ,  ["%1.2f", "%4.0f", "%4.0f", "%4.0f", "%3.0f"])

#tabellen:Winkel
makeTable([[dopplerwinkel[0]],[dopplerwinkel[1]],[dopplerwinkel[2]]], r'{'+r'$\text{Winkel:}\SI{60}{\degree}$'+r'} & {'+r'$\text{Winkel:}\SI{15}{\degree}$'+r'} & {'+r'$\text{Winkel:}\SI{-30}{\degree}$'+r'}' ,'tabdopplerwinkel' , ['S[table-format=2.2]' , 'S[table-format=2.2]' , 'S[table-format=2.2]'] ,  ["%2.2f", "%2.2f", "%2.2f"])

#tabellen: tiefenmessung
makeTable([tiefm45[0],tiefm45[1],tiefm45[2],Vtiefen[0]*100], r'{'+r'$\text{Messtiefe}/\si{\milli\meter}$'+r'} & {'+r'$\Delta f/\si{\hertz}$'+r'} & {'+r'$I_\text{Streu}$'+r'} & {'+r'$v_\text{mom}/\si[per-mode=reciprocal]{\centi\meter\per\second}$'+r'}' ,'tabmtief45' , ['S[table-format=2.2]' , 'S[table-format=4.0]' , 'S[table-format=5.0]' , 'S[table-format=3.0]'] ,  ["%2.2f", "%4.0f", "%5.0f", "%3.0f"])
makeTable([tiefm70[0],tiefm70[1],tiefm70[2],Vtiefen[1]*100], r'{'+r'$\text{Messtiefe}/\si{\milli\meter}$'+r'} & {'+r'$\Delta f/\si{\hertz}$'+r'} & {'+r'$I_\text{Streu}$'+r'} & {'+r'$v_\text{mom}/\si[per-mode=reciprocal]{\centi\meter\per\second}$'+r'}' ,'tabmtief70' , ['S[table-format=2.2]' , 'S[table-format=4.0]' , 'S[table-format=5.0]' , 'S[table-format=3.0]'] ,  ["%2.2f", "%4.0f", "%5.0f", "%3.0f"])

graphen = ["dünn:$\SI{15}{\degree}$","dünn:$\SI{60}{\degree}$","dünn:$\SI{30}{\degree}$","mittel:$\SI{15}{\degree}$","mittel:$\SI{60}{\degree}$","mittel:$\SI{30}{\degree}$","breit:$\SI{15}{\degree}$","breit:$\SI{60}{\degree}$","breit:$\SI{30}{\degree}$"]
makeTable([[r'dünn:$\SI{15}{\degree}$',r'dünn:$\SI{60}{\degree}$',r'dünn:$\SI{30}{\degree}$',r'mittel:$\SI{15}{\degree}$',r'mittel:$\SI{60}{\degree}$',r'mittel:$\SI{30}{\degree}$',r'breit:$\SI{15}{\degree}$',r'breit:$\SI{60}{\degree}$',r'breit:$\SI{30}{\degree}$'],steigung,fehler], r'{'+r'$Graph$'+r'} & \multicolumn{2}{c} {'+r'$Steigung$'+r'}','tabsteigungen' , ['c' , 'S[table-format=2.1]' , 'S[table-format=2.1]'] ,  ["%s", "%2.1f", "%2.1f"])
