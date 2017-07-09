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

es = (np.array(np.genfromtxt("scripts/erstelinse", unpack=True)))
#print("es",es)
erstelinse = np.array([es[1]-es[0],es[2]-es[1],es[3]])
#print("erstelinse",erstelinse)

ws = (np.array(np.genfromtxt("scripts/wasserlinse", unpack=True)))
wasserlinse = np.array([ws[1]-ws[0],ws[2]-ws[1]])

bessel = (np.array(np.genfromtxt("scripts/Bessel", unpack=True)))
#print("bessel",bessel)
bessel = np.array([bessel[1]-bessel[0],bessel[2]-bessel[0],bessel[3]-bessel[1],bessel[3]-bessel[2],bessel[3]-bessel[0],bessel[2]-bessel[1]])

besself = (np.array(np.genfromtxt("scripts/besselfarbe", unpack=True)))
besselfr = np.array([besself[2]-besself[0],besself[3]-besself[0],besself[1]-besself[2],besself[1]-besself[3],besself[1]-besself[0],besself[3]-besself[2]])
besselfb = np.array([besself[4]-besself[0],besself[5]-besself[0],besself[1]-besself[4],besself[1]-besself[5],besself[1]-besself[0],besself[5]-besself[4]])


makeTable([bessel[4],bessel[0],bessel[1],bessel[5]], r'{'+r'$e/\si{\centi\meter}$'+r'} & {'+r'$g_1/\si{\centi\meter}$'+r'} & {'+r'$g_2/\si{\centi\meter}$'+r'} & {'+r'$d/\si{\centi\meter}$'+r'}' ,'tabbessel' , ['S[table-format=2.2]' , 'S[table-format=2.2]', 'S[table-format=2.2]', 'S[table-format=2.2]'] ,  ["%2.2f", "%2.2f", "%2.2f", "%2.2f"])

makeTable([besselfr[4],besselfr[0],besselfr[1],besselfr[5],besselfb[0],besselfb[1],besselfb[5]], r'{'+r'$e/\si{\centi\meter}$'+r'} & {'+r'$g_\text{rot,1}/\si{\centi\meter}$'+r'} & {'+r'$g_\text{rot,2}/\si{\centi\meter}$'+r'} & {'+r'$d_\text{rot}/\si{\centi\meter}$'+r'} & {'+r'$g_\text{blau,1}/\si{\centi\meter}$'+r'} & {'+r'$g_\text{blau,2}/\si{\centi\meter}$'+r'} & {'+r'$d_\text{blau}/\si{\centi\meter}$'+r'}' ,'tabbesself' , ['S[table-format=2.2]' , 'S[table-format=2.2]', 'S[table-format=2.2]', 'S[table-format=2.2]', 'S[table-format=2.2]', 'S[table-format=2.2]', 'S[table-format=2.2]'] ,  ["%2.2f", "%2.2f", "%2.2f", "%2.2f", "%2.2f", "%2.2f", "%2.2f"])


abbe = (np.array(np.genfromtxt("scripts/abbe", unpack=True)))
abbe = np.array([abbe[0]-23.2,abbe[1]-abbe[0],abbe[2]/2.8])
#g',b',V
print("abbe",abbe)
makeTable([abbe[0],abbe[1],abbe[2],abbe[2]/2.8], r'{'+r'$g\'/\si{\centi\meter}$'+r'} & {'+r'$b\'/\si{\centi\meter}$'+r'} & {'+r'$B/\si{\centi\meter}$'+r'}  & {'+r'$V$'+r'}' ,'tababbe' , ['S[table-format=2.1]' , 'S[table-format=3.1]' , 'S[table-format=1.1]', 'S[table-format=1.1]'] ,  ["%2.1f", "%3.1f", "%1.1f", "%1.1f"])

#Funktion

def tosimple(x,y):
    return 1/(1/x + 1/y)

def lin(a,b,x):
    return a*x+b

#rechnen:
#linse
#f1rech = (invert(oneone,erstelinse[0],erstelinse[1]))
f1rech = tosimple(erstelinse[0],erstelinse[1])
f1rech2 = f1rech[np.arange(len(f1rech))!=6]
f1rechm = np.mean(f1rech2)
f1rechstd = stats.sem(f1rech2)

print("yeah",erstelinse[2][0:7])

verhaltm1 = unp.uarray([np.mean(erstelinse[2][0:6]/2.8)],[stats.sem(erstelinse[2][0:6]/2.8)])
print("verhaltm",verhaltm1)
verhaltm2 = unp.uarray([np.mean(erstelinse[1][0:6]/erstelinse[0][0:6])],[stats.sem(erstelinse[1][0:6]/erstelinse[0][0:6])])
print("verhaltm2",verhaltm2)
#wasserlinse
#fwrech = np.array(invert(oneone,wasserlinse[0],wasserlinse[1]))
fwrech = tosimple(wasserlinse[0],wasserlinse[1])
fwrechm = np.mean(fwrech)
fwrechstd = stats.sem(fwrech)
frech = unp.uarray([f1rechm,fwrechm],[f1rechstd,fwrechstd])
print("frech",frech)
#grafisch
#erstelinse
plt.cla()
plt.clf()
i = 0
while i< len(erstelinse[0]):
    plt.plot([0,erstelinse[1][i]],[erstelinse[0][i],0])
    i = i+1

# plt.ylim(0, line(t[-1], *params)+0.1)
# plt.xlim(0, t[-1]*100)
plt.xlabel(r'$g$')
plt.ylabel(r'$b$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'erstelinse')

#wasserlinse
plt.cla()
plt.clf()
i = 0
while i< len(wasserlinse[0]):
    plt.plot([0,wasserlinse[1][i]],[wasserlinse[0][i],0])
    i = i+1

# plt.ylim(0, line(t[-1], *params)+0.1)
# plt.xlim(0, t[-1]*100)
plt.xlabel(r'$g$')
plt.ylabel(r'$b$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'wasserlinse')


#zugehörige Tabellen
#erste
makeTable([erstelinse[0],erstelinse[1],erstelinse[2],f1rech], r'{'+r'$b/\si{\centi\meter}$'+r'} & {'+r'$b/\si{\centi\meter}$'+r'} & {'+r'$B/\si{\centi\meter}$'+r'} & {'+r'$f_\text{100}/\si{\centi\meter}$'+r'}' ,'taberste' , ['S[table-format=2.1]' , 'S[table-format=3.1]' , 'S[table-format=1.1]', 'S[table-format=2.1]'] ,  ["%2.1f", "%3.1f", "%1.1f","%2.1f"])
#wasserlinse
makeTable([wasserlinse[0],wasserlinse[1],fwrech], r'{'+r'$b/\si{\centi\meter}$'+r'} & {'+r'$b/\si{\centi\meter}$'+r'} & {'+r'$f_\text{Wasser}/\si{\centi\meter}$'+r'}' ,'tabwasser' , ['S[table-format=2.1]' , 'S[table-format=3.1]','S[table-format=2.1]'] ,  ["%2.1f", "%3.1f","%2.1f"])

#Brennweite

#print("f1rech",f1rech)
#print("fwrech",fwrech)


#makeTable([f1rech,fwrech], r'{'+r'$f_\text{100}/\si{\centi\meter}$'+r'} & {'+r'$f_\text{Wasser}/\si{\centi\meter}$'+r'}' ,'tabf' , ['S[table-format=2.2]' , 'S[table-format=2.2]'] ,  ["%2.2f", "%2.2f"])

makeTable([erstelinse[1][0:6]/erstelinse[0][0:6],erstelinse[2][0:6]/2.8], r'{'+r'$b/g$'+r'} & {'+r'$B/G$'+r'}' ,'tabverh' , ['S[table-format=1.2]' , 'S[table-format=1.2]'] ,  ["%1.2f", "%1.2f"])



#Bessel

def bes(e,d):
    return (e*e-d*d)/(4*e)


fbessel = bes(bessel[4],bessel[5])
print("fbessel",fbessel)
fbesselr = bes(besselfr[4],besselfr[5])
fbesselb = bes(besselfb[4],besselfb[5])

fbesselm = unp.uarray([np.mean(fbessel),np.mean(fbesselr),np.mean(fbesselb)],[stats.sem(fbessel),stats.sem(fbesselr),stats.sem(fbesselb)])
print("fbesselmall, erst weiss, dann rot, dann blau",fbesselm)



#abbe
unneutig = 1+1/abbe[2]
linfit = curve_fit(lin,unneutig,abbe[0])
linfits1 = [linfit[0],np.sqrt(np.diag(linfit[1]))]
print("linfitsg",linfits1)
plt.cla()
plt.clf()
punkte = np.linspace(0,(1+1/abbe[2][-1])*1.1,1000)
plt.plot(1+(1/abbe[2]),abbe[0], 'rx', label='Die gemessenen Gegenstandsweiten')
plt.plot(punkte,linfits1[0][1]*punkte+linfits1[0][0],label= 'lineare Ausgleichsgerade')
# plt.ylim(0, line(t[-1], *params)+0.1)
# plt.xlim(0, t[-1]*100)
plt.xlabel(r'$1+1/V$')
plt.ylabel(r'$g\'$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'abbeg')


linfit = curve_fit(lin,1+abbe[2],abbe[1])
linfits2 = [linfit[0],np.sqrt(np.diag(linfit[1]))]
print("linfits",linfits2)
plt.cla()
plt.clf()
punkte = np.linspace(0,1+abbe[2][0]*1.1,1000)
plt.plot(1+abbe[2],abbe[1], 'rx', label='Die gemessenen Bildweiten')
plt.plot(punkte,linfits2[0][1]*punkte+linfits2[0][0],label='lineare Ausgleichsgerade')
# plt.ylim(0, line(t[-1], *params)+0.1)
# plt.xlim(0, t[-1]*100)
plt.xlabel(r'$1+V$')
plt.ylabel(r'$b\'$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'abbeb')

fabbe1 = unp.uarray(linfits1[0][1],linfits1[1][1])
fabbe2 = unp.uarray(linfits2[0][1],linfits2[1][1])
fabbem = (fabbe1+fabbe2)/2
atb = fabbem-100/6
print("fabbem",fabbem)
print("deltaabbetheo",atb)
atbperc = abs(atb)/(100/6)
print(atbperc)
