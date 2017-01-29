from table import makeTable
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp

#Temparaturgraphen
Pa, Pb, T1, T2, Leistung = np.genfromtxt("scripts/Daten", unpack=True)
Pa = Pa+1
Pa = Pa *100000
Pb = Pb+1
Pb = Pb *100000
T1 += 273.15
T2 += 273.15
Zeitab = np.linspace(0,1080,len(T1))
#Konstanten
p0 = 5.51*10**(-3)#T = o, P = 1 Bar
k = 1.14
cWasser = 4183#j/(kg*K)


#Die einzelnen Approximationskurven im Vergleich
def Polynom(x, A, B, C):
    return A*x*x+B*x+C

def Bruch1(x, A, B, C):
    return A/(1+B*(x**0.005))

def Bruch2(x, A, B, C, D):
    return (A*x**C)/(1+B*x**C)+D

def linear(x, A, B):
    return A*x+B

#Fehler
paramsPolynomT1, covariancePolynomT1 = curve_fit(Polynom, Zeitab, T1)
paramsPolynomT2, covariancePolynomT2 = curve_fit(Polynom, Zeitab, T2)
errorsPT1 = np.sqrt(np.diag(covariancePolynomT1))
errorsPT2 = np.sqrt(np.diag(covariancePolynomT2))

print('Polynomapproximation T1')
print('A =', paramsPolynomT1[0], 'pm', errorsPT1[0])
print('B =', paramsPolynomT1[1], 'pm', errorsPT1[1])
print('C =', paramsPolynomT1[2], 'pm', errorsPT1[2])
print('Polynomapproximation T2')
print('A =', paramsPolynomT2[0], 'pm', errorsPT2[0])
print('B =', paramsPolynomT2[1], 'pm', errorsPT2[1])
print('C =', paramsPolynomT2[2], 'pm', errorsPT2[2])

#Fehlerarrays
PolynomAT1 = unp.uarray(paramsPolynomT1[0], errorsPT1[0])
PolynomBT1 = unp.uarray(paramsPolynomT1[1], errorsPT1[1])
PolynomAT2 = unp.uarray(paramsPolynomT2[0], errorsPT2[0])
PolynomBT2 = unp.uarray(paramsPolynomT2[1], errorsPT1[1])

plt.cla()
plt.clf()
x_plot = np.linspace(-10, 1100)
#Graphenapproximation
#Graphmit Temperaturen
plt.plot(Zeitab, T1, 'rx', label ="Temperatur von Resservour 1")
plt.plot(Zeitab, T2, 'gx', label = "Temperatur von Resservour 2")
#plt.xlabel(r'$t/\si{\second}$')
#plt.ylabel(r'$T / \si{\kelvin}$')
plt.legend(loc="best")
plt.savefig("Temperaturen.png")

plt.cla()
plt.clf()
#Fitgraph von T1
plt.plot(Zeitab, T1, 'rx', label ="Temperatur von Resservour 1")
plt.plot(x_plot, Polynom(x_plot, *paramsPolynomT1), 'b-', label='Fit durch Polynom 2. Grades', linewidth=1)
plt.legend(loc="best")
plt.savefig("T1.png")

plt.cla()
plt.clf()
#Graphtemparatur2
plt.plot(Zeitab, T2, 'gx', label = "Temperatur von Resservour 2")
plt.plot(x_plot, Polynom(x_plot, *paramsPolynomT2), 'b-', label='Fit durch Polynom 2. Grades', linewidth=1)
plt.legend(loc="best")
plt.savefig("T2.png")


#Güte bestimmen
#Formel
A2T1 = 2*PolynomAT1
A2T2 = 2*PolynomAT2
print('koeffableitungAT1',A2T1)
print('koeffableitungAT2',A2T2)

def Ableitung(x, A, B):
    return A*x+B


#print('AbleitungT1',Ableitung(12*60,A2T1,PolynomBT1))
#print('AbleitungT2',Ableitung(12*60,A2T2,PolynomBT2))
def realGuete(Jim,m1,mkck,cw,N):
    return (m1*cw+mkck)*Jim/N

print('GueteT1bei 2',realGuete(Ableitung(Zeitab[4],A2T1,PolynomBT1),3,660,cWasser,Leistung[2]))
print('GueteT1bei 8',realGuete(Ableitung(Zeitab[8],A2T1,PolynomBT1),3,660,cWasser,Leistung[8]))
print('GueteT1bei 12',realGuete(Ableitung(Zeitab[12],A2T1,PolynomBT1),3,660,cWasser,Leistung[12]))
print('GueteT1bei 16',realGuete(Ableitung(Zeitab[16],A2T1,PolynomBT1),3,660,cWasser,Leistung[16]))

#ideal
print(T1[4]/(T1[4]-T2[4]))
print(T1[8]/(T1[8]-T2[8]))
print(T1[12]/(T1[12]-T2[12]))
print(T1[16]/(T1[16]-T2[16]))
#Rechnung

#Dampfdruckkurve L-Bestimmung
Dampfdruck, covarianceDampfdruck = curve_fit(linear, T2, Pa)
errorsDampfdruck = np.sqrt(np.diag(covarianceDampfdruck))
DampfdruckA = unp.uarray(Dampfdruck[0], errorsDampfdruck[0])
DampfdruckB = unp.uarray(Dampfdruck[1], errorsDampfdruck[1])
#Graph
plt.cla()
plt.clf()
Dampf_plot = np.linspace(273.15+20, 273.15+55, len(T1))
plt.plot(T1, Pb, 'rx', label ="Druck gegen Temaratur")
plt.plot(Dampf_plot, linear(Dampf_plot, *Dampfdruck), 'b-', label='linearer Fit', linewidth=3)
plt.savefig("Dampdruck.png")

print('Dampdrucksteigung',Dampfdruck[0],'pm',errorsDampfdruck[0])
print('Achsenabschnitt',Dampfdruck[1],'pm',errorsDampfdruck[1])



#Massendruchsatz
def Massendurch(Jim2,m2,cw,mkck,L):
    return (m2*cw+mkck)*Jim2/L

print('Massendurchsatz4',Massendurch(Ableitung(4*60,A2T2,PolynomBT2),3,cWasser,660,-8.13*1000/18*Dampfdruck[0]))
print('Massendurchsatz8',Massendurch(Ableitung(8*60,A2T2,PolynomBT2),3,cWasser,660,-8.13*1000/18*Dampfdruck[0]))
print('Massendurchsatz12',Massendurch(Ableitung(12*60,A2T2,PolynomBT2),3,cWasser,660,-8.13*1000/18*Dampfdruck[0]))
print('Massendurchsatz16',Massendurch(Ableitung(16*60,A2T2,PolynomBT2),3,cWasser,660,-8.13*1000/18*Dampfdruck[0]))
#Kompressorleistung
