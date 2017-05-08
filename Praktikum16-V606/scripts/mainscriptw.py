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


#1. Messwerte einlesen
Kurvenmesswerte = np.genfromtxt('scripts/Kurvendaten', unpack=True)
C6O12Pr2 = np.genfromtxt('scripts/C6O12Pr2', unpack=True)
Dy2O3 = np.genfromtxt('scripts/Dy2O3', unpack=True)
Gd2O3 = np.genfromtxt('scripts/Gd2O3', unpack=True)
Nd2O3 = np.genfromtxt('scripts/Nd2O3', unpack=True)
Basisdaten = np.genfromtxt('scripts/Basisdatenstoffe')
#y = 900*np.exp(-1*a*abs((x-35.17)**1))+b
#(ln((y-b)/900)/-a)+35.17 = (x-35.17)

#ln

#Fitfunktion der Resonanzkurve
#def Resonanzkurve1(x, a, b):
#	return 1/np.sqrt((1-(2*np.pi*x*a)**2)**2+(b*2*np.pi*x)**2)
def Resonanzkurve2(x,a,b):
    return 900*np.exp(-1*a*abs((x-35.17)**1))+b
#alt 900
#gefittete Kurve
Kurvenfitpunkte = np.linspace(Kurvenmesswerte[0][0],Kurvenmesswerte[0][-1],1000)
Kurvenfit = curve_fit(Resonanzkurve2,Kurvenmesswerte[0],Kurvenmesswerte[1])
Kurvenfit = [Kurvenfit[0],np.sqrt(np.diag(Kurvenfit[1]))]

print("gefittete Parameter")
print("Vorfaktor = 900")
print("Symmetrieachse der Funktion bei 35.17")
print("a =",Kurvenfit[0][0])
print("b =",Kurvenfit[0][1])


plt.plot(Kurvenmesswerte[0], Kurvenmesswerte[1], 'gx', label='Darstellung der Messergebnisse')
#plt.plot(Kurvenfitpunkte,Resonanzkurve2(Kurvenfitpunkte,1.2,-35.15,25,900))
#plt.plot(Kurvenfitpunkte,Resonanzkurve2(Kurvenfitpunkte,Kurvenfit[0][0],Kurvenfit[0][1],Kurvenfit[0][2],Kurvenfit[0][3]))
plt.plot(Kurvenfitpunkte,Resonanzkurve2(Kurvenfitpunkte,Kurvenfit[0][0],Kurvenfit[0][1]),label='exponentieller Fit')
#plt.ylim(0, line(t[-1], *params)+0.1)
#plt.xlim(0, t[-1]*100)
plt.xlabel(r'$f/\si{\hertz}$')
plt.ylabel(r'$U/\si{\milli\volt}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'Resonanzkurve')
plt.cla()
plt.clf()

#Bestimmung der Güte
Hochpunkt = Resonanzkurve2(35.17,Kurvenfit[0][0],Kurvenfit[0][1])
Vplus = -np.log(((1/np.sqrt(2))*Hochpunkt-Kurvenfit[0][1])/900)/Kurvenfit[0][0]+35.17
print("Hochpunkt",Hochpunkt)
print("Vplus",Vplus)
Guete = 35.17/(2* abs(Vplus-35.17))
print("Güte",Guete)


C6O12Pr2 = np.array(C6O12Pr2)
Nd2O3 = np.array(Nd2O3)
Gd2O3 = np.array(Gd2O3)
Dy2O3 = np.array(Dy2O3)



#Suszeptibilität praktische Auswertung
#def deltaR(R3,delL,L):
#	return delL*R3/(2*L)
 #über deltaR
def querschnitt(Laenge,normaldichte,masse):
	return masse/(Laenge*normaldichte)

def Suszeptibilitaet(delR,R3,Q):
	return 2*(0.005*delR)/(998+0.005*R3)*(0.0000866/Q)

SusGd2O3 = Suszeptibilitaet(Gd2O3[5],Gd2O3[1],querschnitt(Basisdaten[3][1],Basisdaten[3][3],Basisdaten[3][2]))
print("SusGd2O3",SusGd2O3)

SusNd2O3 = Suszeptibilitaet(Nd2O3[5],Nd2O3[1],querschnitt(Basisdaten[2][1],Basisdaten[2][3],Basisdaten[2][2]))
print("SusNd2O3",SusNd2O3)

SusDy2O3 = Suszeptibilitaet(Dy2O3[5],Dy2O3[1],querschnitt(Basisdaten[1][1],Basisdaten[1][3],Basisdaten[1][2]))
print("SusDy2O3",SusDy2O3)

#Für die querschnittsfläche der probe wird die fläche der probe verwendet
SusC6O12Pr2 = Suszeptibilitaet(C6O12Pr2[5],C6O12Pr2[1],0.0000866)
print("SusC6O12Pr2",SusC6O12Pr2)


SusGd2O3M = unp.uarray(np.mean(SusGd2O3),np.std(SusGd2O3))
SusNd2O3M = unp.uarray(np.mean(SusNd2O3),np.std(SusNd2O3))
SusDy2O3M = unp.uarray(np.mean(SusDy2O3),np.std(SusDy2O3))

makeTable([[unp.nominal_values(SusNd2O3M)],[unp.std_devs(SusNd2O3M)],[unp.nominal_values(SusGd2O3M)],[unp.std_devs(SusGd2O3M)],[unp.nominal_values(SusDy2O3M)],[unp.std_devs(SusDy2O3M)]], r'\multicolumn{2}{c}{$\chi_{Nd_2O_3}$} & \multicolumn{2}{c}{$\chi_{Gd_2O_3}$} & \multicolumn{2}{c}{$\chi_{Dy_2O_3}$}', 'SusR',[r'S[table-format=1.5]',  r'@{${}\pm{}$} S[table-format=1.5]',r'S[table-format=1.5]', r'@{${}\pm{}$} S[table-format=1.5]', r' S[table-format=1.5]', r'@{${}\pm{}$} S[table-format=1.5]'], ["%1.5f", "%1.5f", "%1.5f", "%1.5f", "%1.5f", "%1.5f"])


#Über die Spannungsdifferenz

#eingangsspannung der brückenspannung 0.8V
def suszintibilitaetU(Q,Ubr):
	return 4*(0.0000866/Q)*(Ubr/0.8)

SusGd2O3U = suszintibilitaetU(querschnitt(Basisdaten[3][1],Basisdaten[3][3],Basisdaten[3][2]),0.001*Gd2O3[3])
print("SusGd2O3U",SusGd2O3U)

SusNd2O3U = suszintibilitaetU(querschnitt(Basisdaten[2][1],Basisdaten[2][3],Basisdaten[2][2]),0.001*Nd2O3[3])
print("SusNd2O3U",SusNd2O3U)

SusDy2O3U = suszintibilitaetU(querschnitt(Basisdaten[1][1],Basisdaten[1][3],Basisdaten[1][2]),0.001*Dy2O3[3])
print("SusDy2O3U",SusDy2O3U)

SusC6O12Pr2U = suszintibilitaetU(0.0000866,0.001*C6O12Pr2[3])
print("SusC6O12Pr2U",SusC6O12Pr2U)

SusGd2O3UM = unp.uarray(np.mean(SusGd2O3U),np.std(SusGd2O3U))
SusNd2O3UM = unp.uarray(np.mean(SusNd2O3U),np.std(SusNd2O3U))
SusDy2O3UM = unp.uarray(np.mean(SusDy2O3U),np.std(SusDy2O3U))


makeTable([[unp.nominal_values(SusNd2O3UM)],[unp.std_devs(SusNd2O3UM)],[unp.nominal_values(SusGd2O3UM)],[unp.std_devs(SusGd2O3UM)],[unp.nominal_values(SusDy2O3UM)],[unp.std_devs(SusDy2O3UM)]], r'\multicolumn{2}{c}{$\chi_{Nd_2O_3}$} & \multicolumn{2}{c}{$\chi_{Gd_2O_3}$} & \multicolumn{2}{c}{$\chi_{Dy_2O_3}$}', 'SusU',[r'S[table-format=1.5]',  r'@{${}\pm{}$} S[table-format=1.5]',r'S[table-format=1.5]', r'@{${}\pm{}$} S[table-format=1.5]', r' S[table-format=1.5]', r'@{${}\pm{}$} S[table-format=1.5]'], ["%1.5f", "%1.5f", "%1.5f", "%1.5f", "%1.5f", "%1.5f"])



#Suszeptibilität theoretische Berechnung

uB = 0.5 * (const.value("electron volt")/const.value("electron mass"))*const.value("Planck constant")
#J:Nd3+ = 4.5
#J:Gd3+ = -4.5
#J:Dy3+ = 9.5

def Gj(J,L,S):
	return (3*J*(J+1)+S*(S+1)-L*(L+1))/(2*J*(J*1))

def N(m,M,l,Q):
    return const.value("Avogadro constant")*m/(M*l*Q)

#https://pubchem.ncbi.nlm.nih.gov/compound/159373#section=Top

NNd2O3 = N(Basisdaten[2][2],0.336481,Basisdaten[2][1],querschnitt(Basisdaten[2][1],Basisdaten[2][3],Basisdaten[2][2]))
#https://pubchem.ncbi.nlm.nih.gov/compound/159427
NGd2O3 = N(Basisdaten[3][2],0.362497,Basisdaten[3][1],querschnitt(Basisdaten[3][1],Basisdaten[3][3],Basisdaten[3][2]))
#https://pubchem.ncbi.nlm.nih.gov/compound/159370
NDy2O3 = N(Basisdaten[1][2],0.372997,Basisdaten[1][1],querschnitt(Basisdaten[1][1],Basisdaten[1][3],Basisdaten[1][2]))




def Sus(Gj,N,J):
	return const.value("mag. constant")*(uB**2)*(Gj**2)*N*J*(J+1)/(3*const.value("Boltzmann constant")*(293.15))

GjNd2O3 = Gj(4.5,6,1.5)
GjGd2O3 = Gj(-3.5,0,3.5)
GjDy2O3 = Gj(7.5,5,2.5)



SusDy2O3T = np.array([Sus(GjDy2O3,NDy2O3,7.5), Sus(GjNd2O3,NNd2O3,4.5), Sus(GjGd2O3,NGd2O3,-3.5)])
print("theorie",SusDy2O3T)
#SusNd2O3T = np.array(Sus(GjNd2O3,NNd2O3,4.5),0)
#SusGd2O3T = np.array(Sus(GjGd2O3,NGd2O3,-3.5),0)

makeTable([[SusDy2O3T[0]], [SusDy2O3T[1]], [SusDy2O3T[2]]], r'{'+r'$\chi_{Nd_2O_3}$'+r'} & {'+r'$\chi_{Gd_2O_3}$'+r'} & {'+r'$\chi_{Dy_2O_3}$'+r'}' ,'SusT' , ['S[table-format=0.5]' , 'S[table-format=0.5]', 'S[table-format=0.5]' ] ,  ["%0.5f", "%0.5f" , "%0.5f"])




#Tabellen
    #Tabelle der Messwerte der Resonanzkurve
    #1.Teil

makeTable([Kurvenmesswerte[0] [0:len(Kurvenmesswerte[0])//2],Kurvenmesswerte[1] [0:len(Kurvenmesswerte[0])//2] ], r'{'+r'$f/\si{\hertz}$'+r'} & {'+r'$U/\si{\milli\volt}$'+r'}' ,'tabKurvenergebnisse1' , ['S[table-format=2.1]' , 'S[table-format=3.0]'] ,  ["%2.1f", "%3.0f"])
   #2.Teil
makeTable([Kurvenmesswerte[0][(len(Kurvenmesswerte[0]))//2+1:(len(Kurvenmesswerte[0]))] ,Kurvenmesswerte[1][(len(Kurvenmesswerte[0]))//2+1:(len(Kurvenmesswerte[0]))]] , r'{'+r'$f/\si{\hertz}$'+r'} & {'+r'$U/\si{\milli\volt}$'+r'}' ,'tabKurvenergebnisse2' , ['S[table-format=2.1]' , 'S[table-format=3.0]'] ,  ["%2.1f", "%3.0f"])


#Tabelle der basisdatenstoffe
#makeTable(Basisdaten[0], Basisdaten[1], Basisdaten[2], Basisdaten[3], r'{'+r'$$'+r'} & {'+r'$U/\si{\milli\volt}$'+r'}' ,'tabKurvenergebnisse1' , ['S[table-format=2.1]' , 'S[table-format=3.0]'] ,  ["%2.1f", "%3.0f"])


#Stofftabellenmesswerte
#Nd2O3
makeTable([Nd2O3[0], Nd2O3[2], Nd2O3[3], Nd2O3[1], Nd2O3[4], Nd2O3[5]], r'{'+r'$U_\text{alt}/\si{\milli\volt}$'+r'} & {'+r'$U_\text{neu}/\si{\milli\volt}$'+r'} & {'+r'$\Delta U/\si{\milli\volt}$'+r'} & {'+r'$R_3 \text{Einstellung}_\text{alt}$'+r'} & {'+r'$R_3 \text{Einstellung}_\text{neu}$'+r'}& {'+r'$\Delta R_3 \text{Einstellung}$'+r'}' ,'tabNd2O3' , ['S[table-format=1.2]' , 'S[table-format=1.2]',  'S[table-format=1.2]',  'S[table-format=3.0]',  'S[table-format=3.0]',  'S[table-format=3.0]'] ,  ["%1.2f", "%1.2f", "%1.2f", "%3.0f", "%3.0f", "%3.0f"])
#Dy2O3
makeTable([Dy2O3[0], Dy2O3[2], Dy2O3[3], Dy2O3[1], Dy2O3[4], Dy2O3[5]], r'{'+r'$U_\text{alt}/\si{\milli\volt}$'+r'} & {'+r'$U_\text{neu}/\si{\milli\volt}$'+r'} & {'+r'$\Delta U/\si{\milli\volt}$'+r'} & {'+r'$R_3 \text{Einstellung}_\text{alt}$'+r'} & {'+r'$R_3 \text{Einstellung}_\text{neu}$'+r'}& {'+r'$\Delta R_3 \text{Einstellung}$'+r'}' ,'tabDy2O3' , ['S[table-format=1.2]' , 'S[table-format=1.2]',  'S[table-format=1.2]',  'S[table-format=3.0]',  'S[table-format=3.0]',  'S[table-format=3.0]'] ,  ["%1.2f", "%1.2f", "%1.2f", "%3.0f", "%3.0f", "%3.0f"])
#Gd2O3
makeTable([Gd2O3[0], Gd2O3[2], Gd2O3[3], Gd2O3[1], Gd2O3[4], Gd2O3[5]], r'{'+r'$U_\text{alt}/\si{\milli\volt}$'+r'} & {'+r'$U_\text{neu}/\si{\milli\volt}$'+r'} & {'+r'$\Delta U/\si{\milli\volt}$'+r'} & {'+r'$R_3 \text{Einstellung}_\text{alt}$'+r'} & {'+r'$R_3 \text{Einstellung}_\text{neu}$'+r'}& {'+r'$\Delta R_3 \text{Einstellung}$'+r'}' ,'tabGd2O3' , ['S[table-format=1.2]' , 'S[table-format=1.2]',  'S[table-format=1.2]',  'S[table-format=3.0]',  'S[table-format=3.0]',  'S[table-format=3.0]'] ,  ["%1.2f", "%1.2f", "%1.2f", "%3.0f", "%3.0f", "%3.0f"])
#C6O12Pr2
makeTable([C6O12Pr2[0], C6O12Pr2[2], C6O12Pr2[3], C6O12Pr2[1], C6O12Pr2[4], C6O12Pr2[5]], r'{'+r'$U_\text{alt}/\si{\milli\volt}$'+r'} & {'+r'$U_\text{neu}/\si{\milli\volt}$'+r'} & {'+r'$\Delta U/\si{\milli\volt}$'+r'} & {'+r'$R_3 \text{Einstellung}_\text{alt}$'+r'} & {'+r'$R_3 \text{Einstellung}_\text{neu}$'+r'}& {'+r'$\Delta R_3 \text{Einstellung}$'+r'}' ,'tabNd2O3' , ['S[table-format=1.2]' , 'S[table-format=1.2]',  'S[table-format=1.2]',  'S[table-format=3.0]',  'S[table-format=3.0]',  'S[table-format=3.0]'] ,  ["%1.2f", "%1.2f", "%1.2f", "%3.0f", "%3.0f", "%3.0f"])


#tabelle mit spindaten:
spindaten = [["$Nd_2O_3$","$Gd_2O_3$","$Dy_2O_3$"],[1.5,3.5,2.5],[6,0,5],[4.5,-3.5,7.5]]
print("spindaten",spindaten)
makeTable([spindaten[0], spindaten[1], spindaten[2], spindaten[3]], r'{'+r'$Probenstoff$'+r'} & {'+r'$S$'+r'} & {'+r'$L$'+r'} & {'+r'$J$'+r'}','tabspins' , ['c' , 'S[table-format=1.2]',  'S[table-format=1.2]',  'S[table-format=3.0]'] ,  ["%s", "%1.2f", "%1.2f", "%3.0f"])
