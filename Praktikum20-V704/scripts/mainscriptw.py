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
BetaJ = np.array(np.genfromtxt('scripts/BetaJ.txt',unpack=True))
BetaC = np.array(np.genfromtxt('scripts/Beta.txt',unpack=True))
Nullabfall = (968+1034)/2000
Nullabfallb = 1028 /2000
def linear(a,x,b):
    return a*x+b

#Ausgleichsgeraden
punkte = np.linspace(0,Kupfer[0][-1]*1.1,1000)
lin = curve_fit(linear,Kupfer[0],np.log((Kupfer[2]/Kupfer[1])-Nullabfall),sigma = np.log(np.sqrt((Kupfer[2]/Kupfer[1])-Nullabfall)))
linfitsk = [lin[0],np.sqrt(np.diag(lin[1]))]
linfitsk = unp.uarray(linfitsk[0],linfitsk[1])
print("linearerFit,Kupfer:",linfitsk)
muk = -linfitsk[0]
N0k = unp.exp(linfitsk[1])
print("mucomcaesium137prakkupfer:",muk)
plt.cla()
plt.clf()
plt.plot(Kupfer[0],np.log((Kupfer[2]/Kupfer[1])-Nullabfall), 'gx', label='gemessene Werte')
plt.plot(punkte,linear(unp.nominal_values(linfitsk[0]),punkte,unp.nominal_values(linfitsk[1])),label = 'linearer Fit')
plt.xlabel(r'$d/\si{\milli\meter}$')
plt.ylabel(r'$N/t\si{\per\second}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'Kupfer')

punkte = np.linspace(0,Eisen[0][-1]*1.1,1000)
lin = curve_fit(linear,Eisen[0],np.log((Eisen[2]/Eisen[1])-Nullabfall),sigma = np.log(np.sqrt((Eisen[2]/Eisen[1])-Nullabfall)))
linfitse = [lin[0],np.sqrt(np.diag(lin[1]))]
linfitse = unp.uarray(linfitse[0],linfitse[1])
mu = -linfitse[0]
N0 = unp.exp(linfitse[1])
print("linearerFit,Eisen:",linfitse)
print("mucomcaesium137prakeisen:",mu)
plt.cla()
plt.clf()
plt.plot(Eisen[0],np.log((Eisen[2]/Eisen[1])-Nullabfall), 'gx', label='gemessene Werte')
plt.plot(punkte,linear(unp.nominal_values(linfitse[0]),punkte,unp.nominal_values(linfitse[1])),label = 'linearer Fit')
plt.xlabel(r'$d/\si{\milli\meter}$')
plt.ylabel(r'$N/t\si{\per\second}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'Eisen')

#b)
def sigma(eps):
    return 2*np.pi*((2.82*10**(-15))**2)*(((1+eps)/(eps**2))*((2*(1+eps))/(1+2*eps)-(1/eps)*np.log(1+2*eps))+(1/(2*eps))*np.log(1+2*eps)-(1+3*eps)/((1+2*eps)**2))

def mucom(eps,z,M,rho):
    return z*const.value("Avogadro constant")*rho*sigma(eps)/M
mucomk = mucom(1.295,29,0.063546,8920)/1000#quelle von M und rho_ wikipedia und deren quellen 1/mm
print("Mucomkupfer:",mucomk)

mucome = mucom(1.295,26,0.055845,7874)/1000#quelle von M und rho_ wikipedia und deren quellen 1/mm
print("Mucomeisen:",mucome)

#mucomCs = mucom(1.295,29,63.546,8.92)#quelle von M und rho_ wikipedia und deren quellen
#print("Mucomkupfer:",mucomCs)
#betastrahlung

#linb1 = curve_fit(linear,BetaC[0]*0.001*2710,np.log((BetaC[2]/Beta[1])-Nullabfallb),sigma = np.log(np.sqrt((BetaC[2]/BetaC[1])-Nullabfallb)))
#linfitsb1 = [linb1[0],np.sqrt(np.diag(linb1[1]))]
plt.cla()
plt.clf()
plt.plot(BetaC[0]*0.001*2710,np.log((BetaC[2]/BetaC[1])), 'gx', label='gemessene Werte')
#plt.plot(punkte,linear(linfitsk[0][0],punkte,linfitsk[0][1]),label = 'linearer Fit')
plt.xlabel(r'$R/\si{\kilogram\per\square\meter}$')
plt.ylabel(r'$N/t\si{\per\second}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'BetaC')


punkte = np.linspace(0,BetaJ[0][-1]*1.1*0.001*2710,1000)
linb1 = curve_fit(linear,BetaJ[0][0:5]*0.001*2710,np.log((BetaJ[2][0:5]/BetaJ[1][0:5])),sigma = np.log(np.sqrt((BetaJ[2][0:5]/BetaJ[1][0:5]))))
linfitsb1 = [linb1[0],np.sqrt(np.diag(linb1[1]))]
print("linearerFit1 von beta,Joshua",linfitsb1)
linfitsb1 = unp.uarray(linfitsb1[0],linfitsb1[1])
linb2 = curve_fit(linear,BetaJ[0][6:9]*0.001*2710,np.log((BetaJ[2][6:9]/BetaJ[1][6:9])),sigma = np.log(np.sqrt((BetaJ[2][6:9]/BetaJ[1][6:9]))))
linfitsb2 = [linb2[0],np.sqrt(np.diag(linb2[1]))]
print("linearerFit2 von beta,Joshua",linfitsb2)
linfitsb2 = unp.uarray(linfitsb2[0],linfitsb2[1])
plt.cla()
plt.clf()
plt.plot(BetaJ[0]*0.001*2710,np.log((BetaJ[2]/BetaJ[1])), 'gx', label='gemessene Werte')
plt.plot(punkte,linear(unp.nominal_values(linfitsb1[0]),punkte,unp.nominal_values(linfitsb1[1])))
plt.plot(punkte,linear(unp.nominal_values(linfitsb2[0]),punkte,unp.nominal_values(linfitsb2[1])))
plt.xlabel(r'$R/\si{\kilogram\per\square\meter}$')
plt.ylabel(r'$N/t\si{\per\second}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'BetaJ')

#Schnittstelle
Rmax = 0.1*(linfitsb2[1]-linfitsb1[1])/(linfitsb1[0]-linfitsb2[0])
print("Rmax",Rmax)
Emax = 1.92*((Rmax**2+0.22*Rmax)**(0.5))
print("Emax",Emax)
#Tabellen mit den Daten
#gamma
makeTable([Kupfer[0],Kupfer[1],Kupfer[2]], r'{'+r'$d_\text{Absorber}/\si{\milli\meter}$'+r'} & {'+r'$t_\text{Mess}/\si{\second}$'+r'} & {'+r'$N_\text{Wechsel}$'+r'}' ,'tabgammakupfer' , ['S[table-format=2.1]' , 'S[table-format=3.0]' , 'S[table-format=5.0]'] ,  ["%2.1f", "%3.0f", "%5.0f"])
makeTable([Eisen[0],Eisen[1],Eisen[2]], r'{'+r'$d_\text{Absorber}/\si{\milli\meter}$'+r'} & {'+r'$t_\text{Mess}/\si{\second}$'+r'} & {'+r'$N_\text{Wechsel}$'+r'}' ,'tabgammaeisen' , ['S[table-format=2.1]' , 'S[table-format=3.0]' , 'S[table-format=5.0]'] ,  ["%2.1f", "%3.0f", "%5.0f"])

#beta
makeTable([BetaJ[0]*1000,BetaJ[1],BetaJ[2]], r'{'+r'$d_\text{Absorber}/\si{\micro\meter}$'+r'} & {'+r'$t_\text{Mess}/\si{\second}$'+r'} & {'+r'$N_\text{Wechsel}$'+r'}' ,'tabgammabetaJ' , ['S[table-format=3.0]' , 'S[table-format=3.0]' , 'S[table-format=4.0]'] ,  ["%3.0f", "%3.0f", "%4.0f"])



#ergebnisse
#gamma
mat = ["Kupfer","Eisen"]
daempfung = [unp.nominal_values(muk),unp.nominal_values(mu)]
daempfungerr = [unp.std_devs(muk),unp.std_devs(mu)]
N0 = [unp.nominal_values(N0k),unp.nominal_values(N0)]
print(unp.std_devs(N0))
N0err = [unp.std_devs(N0k),unp.std_devs(N0)]
daempfungt = [mucomk,mucome]
print(mat)
print(daempfung)
print(daempfungerr)
print(N0)
print(N0err)
print(daempfungt)

makeTable([mat,daempfung,daempfungerr,N0,daempfungt], r'{'+r'$\text{Absorbermaterial}$'+r'} & \multicolumn{2}{c}{$\mu/\si[per-mode=reciprocal]{\per\milli\meter}$} & {$N_0$} & {$\mu_\text{ger.}/\si[per-mode=reciprocal]{\per\milli\meter}$}', 'ergebnisse',['c',r'S[table-format=1.3]',  r'@{${}\pm{}$} S[table-format=1.3]', r'S[table-format=4.0]',r'S[table-format=1.3]'], ["%s","%1.3f", "%1.3f", "%4.0f","%1.3f"])

makeTable([[unp.nominal_values(Rmax)],[unp.std_devs(Rmax)],[unp.nominal_values(Emax)],[unp.std_devs(Emax)]], r'\multicolumn{2}{c}{'+r'$\text{Rmax}/\si[per-mode=reciprocal]{\gram\per\square\centi\meter}$'+r'} & \multicolumn{2}{c}{$\mu/{\mega\electronvol}$}', 'ergebnisse2',[r'S[table-format=1.3]',  r'@{${}\pm{}$} S[table-format=1.3]', r'S[table-format=1.3]',  r'@{${}\pm{}$} S[table-format=1.3]'], ["%1.3f", "%1.3f", "%1.3f","%1.3f"])
