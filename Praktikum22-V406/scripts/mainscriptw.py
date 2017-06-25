from table import makeTable
from table import makeNewTable
from linregress import linregress
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
# makeNewTable([convert((r'$c_\text{1}$',r'$c_\text{2}$',r'$T_{\text{A}1}$',r'$T_{\text{A}2}$',r'$\alpha$',r'$D_1$',r'$D_2$',r'$A_1$',r'$A_2$',r'$A_3$',r'$A_4$'),strFormat),convert(np.array([paramsGes2[0],paramsGes1[0],deltat2*10**6,deltat1*10**6,-paramsDaempfung[0]*2,4.48*10**-6 *paramsGes1[0]/2*10**3, 7.26*10**-6 *paramsGes1[0]/2*10**3, (VierteMessung-2*deltat2*10**6)[0]*10**-6 *1410 /2*10**3, unp.uarray((VierteMessung[1]-VierteMessung[0])*10**-6 *1410 /2*10**3, 0), unp.uarray((VierteMessung[2]-VierteMessung[1])*10**-6 *2500 /2*10**3, 0),unp.uarray((VierteMessung[3]-VierteMessung[2])*10**-6 *1410 /2*10**3, 0)]),unpFormat,[[r'\meter\per\second',"",True],[r'\meter\per\second',"",True],[r'\micro\second',"",True],[r'\micro\second',"",True],[r'\per\meter',"",True],[r'\milli\meter',"",True],[r'\milli\meter',"",True],[r'\milli\meter',"",True],[r'\milli\meter',r'1.3f',True],[r'\milli\meter',r'1.3f',True],[r'\milli\meter',r'2.2f',True]]),convert(np.array([2730,2730]),floatFormat,[r'\meter\per\second','1.0f',True])+convert((r'-',r'-'),strFormat)+convert(unp.uarray([57,6.05,9.9],[2.5,0,0]),unpFormat,[[r'\per\meter',"",True],[r'\milli\meter',r'1.2f',True],[r'\milli\meter',r'1.2f',True]])+convert((r'-',r'-',r'-',r'-'),strFormat),convert(np.array([(2730-paramsGes2[0])/2730*100,(2730-paramsGes1[0])/2730*100]),unpFormat,[r'\percent','',True])+convert((r'-',r'-'),strFormat)+convert(np.array([(-paramsDaempfung[0]*2-unp.uarray(57,2.5))/unp.uarray(57,2.5)*100,(4.48*10**-6 *paramsGes1[0]/2*10**3-6.05)/6.05*100, (-7.26*10**-6 *paramsGes1[0]/2*10**3+9.90)/9.90*100]),unpFormat,[r'\percent','',True])+convert((r'-',r'-',r'-',r'-'),strFormat)],r'{Wert}&{gemessen}&{Literaturwert\cite{cAcryl},\cite{alphaAcryl}}&{Abweichung}','Ergebnisse', ['c ','c',r'c','c'])

einzelspalt = (np.array(np.genfromtxt("scripts/einzelspalt", unpack=True)))-0.36
einzelspalt = np.array([einzelspalt[0],einzelspalt[0]/1265, einzelspalt[1]])
ds1 = (np.array(np.genfromtxt("scripts/ds1", unpack=True)))-0.36
ds2 = (np.array(np.genfromtxt("scripts/ds2", unpack=True)))-0.36
ds1 = np.array([ds1[0],ds1[0]/1265,ds1[1]])
ds2 = np.array([ds2[0],ds2[0]/1265,ds2[1]])

def intens(phi,b,d,lamda):
    return ((np.cos(np.pi*d*np.sin(phi)/lamda))**2)*((lamda/(np.pi*b*np.sin(phi)))**2)*((np.sin(np.pi*b*np.sin(phi)/lamda))**2)

#b = sin
l= np.pi/(635*10**-9)
#def einzel(x,a,b):
#    return ((a*b)**2)*(1/((b*x)**2))*(np.sin(b*x))**2
def einzel(x,A,B):
    return A*(np.sin(B*x)**2)/(x**2)

x1 = np.linspace(-0.017,0.017,1000)
fitted = curve_fit(einzel,einzelspalt[1],einzelspalt[2])
fitted = [fitted[0],np.sqrt(np.diag(fitted[1]))]

plt.cla()
plt.clf()
plt.plot(einzelspalt[1], einzelspalt[2], 'gx', label='Daten von einzelspalt')
plt.plot(x1,einzel(x1,fitted[0][0],fitted[0][1]),label = 'Fit')
fitdata = unp.uarray(fitted[0],fitted[1])
fitdata[0] = (unp.sqrt(fitdata[0]))*(np.pi/(635*10**-9))
fitdata[1] = fitdata[1]*(635*10**-9)/(np.pi)
print("gefittete parameter",fitdata)
#plt.plot(BackwardsVNominal*100, DeltaVBackwardsNominal, 'rx', label='Daten mit Bewegungsrichtung vom Mikrofon weg')
#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(0, t[-1]*100)
plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
plt.ylabel(r'$\Delta f / \si{\hertz}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'einzelspalt')


plt.cla()
plt.clf()
plt.plot(ds1[1], ds1[2], 'gx', label='Daten von doppelspalt 1')
plt.plot(x1,intens(x1,0.00015,0.00029,635*10**(-9))*5000)
#plt.plot(x1,intens(x1,0.0001,0.0004,635*10**(-9))*5000)
#plt.plot(BackwardsVNominal*100, DeltaVBackwardsNominal, 'rx', label='Daten mit Bewegungsrichtung vom Mikrofon weg')
#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(0, t[-1]*100)
plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
plt.ylabel(r'$\Delta f / \si{\hertz}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'ds1')

plt.cla()
plt.clf()
plt.plot(ds2[1], ds2[2], 'gx', label='Daten von doppelspalt 2')
plt.plot(x1,intens(x1+(1/1256),0.0001,0.0004,635*10**(-9))*1300)
#plt.plot(BackwardsVNominal*100, DeltaVBackwardsNominal, 'rx', label='Daten mit Bewegungsrichtung vom Mikrofon weg')
#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(0, t[-1]*100)
plt.xlabel(r'$v/\si{\centi\meter\per\second}$')
plt.ylabel(r'$\Delta f / \si{\hertz}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'ds2')


makeTable([einzelspalt[0],einzelspalt[1]*180/(np.pi),einzelspalt[2]], r'{'+r'$\Delta x/\si{\milli\meter}$'+r'} & {'+r'$\Delta x /\si{\degree}$'+r'} & {'+r'$I/\si{\nano\ampere}$'+r'}' ,'tabeinzelspalt' , ['S[table-format=2.1]' , 'S[table-format=1.3]' , 'S[table-format=2.1]'] ,  ["%2.1f", "%1.3f", "%2.1f"])
makeTable([ds1[0],ds1[1]*180/(np.pi),ds1[2]], r'{'+r'$\Delta x/\si{\milli\meter}$'+r'} & {'+r'$\Delta x /\si{\degree}$'+r'} & {'+r'$I/\si{\nano\ampere}$'+r'}' ,'tabds1' , ['S[table-format=2.1]' , 'S[table-format=1.3]' , 'S[table-format=4.0]'] ,  ["%2.1f", "%1.3f", "%4.0f"])
makeTable([ds2[0],ds2[1]*180/(np.pi),ds2[2]], r'{'+r'$\Delta x/\si{\milli\meter}$'+r'} & {'+r'$\Delta x /\si{\degree}$'+r'} & {'+r'$I/\si{\nano\ampere}$'+r'}' ,'tabds1' , ['S[table-format=2.1]' , 'S[table-format=1.3]' , 'S[table-format=4.0]'] ,  ["%2.1f", "%1.3f", "%4.0f"])
