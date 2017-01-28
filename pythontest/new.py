from table import makeTable
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp
"""
p = np.array([1, 2, 3, 4, 5])
p = p**p
p = np.cos(p)


def poly(y):
    return np.cos(np.exp(np.cos(y)))


Zahl, zeitvor, zeitruck = np.genfromtxt("Vmessung", unpack=True)
plt.cla()
plt.clf()
x = np.linspace(-100, 100, 1000)
T = np.linspace(-100,100,len(zeitruck))
P = np.linspace(-100, 100, len(p))
plt.plot(T, np.sin(zeitruck))
plt.plot(P, p)
plt.plot(x, poly(x))
plt.show()
"""
#Temparaturgraphen
Pa, Pb, T1, T2, Leistung = np.genfromtxt("Daten", unpack=True)
Pa = Pa+1
Pb = Pb+1
T1 += 273.15
T2 += 273.15
Zeitab = np.linspace(0,18,len(T1))
plt.plot(Zeitab, T1)
plt.plot(Zeitab, T2)

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

#Fehler
paramsPolynomT1, covariancePolynomT1 = curve_fit(Polynom, Zeitab, T1)
paramsPolynomT2, covariancePolynomT2 = curve_fit(Polynom, Zeitab, T2)
"""
paramsBruch1T1, covarianceBruch1T1 = curve_fit(Bruch1, Zeitab, T1)
#paramsBruch1T2, covarianceBruch1T2 = curve_fit(Bruch1, Zeitab, T2)
#paramsBruch2T1, covarianceBruch2T1 = curve_fit(Bruch2, Zeitab, T1)
#paramsBruch2T2, covarianceBruch2T2 = curve_fit(Bruch2, Zeitab, T2)
"""

errorsPT1 = np.sqrt(np.diag(covariancePolynomT1))
#errorsB1T1 = np.sqrt(np.diag(covarianceBruch1T1))
#errorsB2T1 = np.sqrt(np.diag(covarianceBruch2T1))
errorsPT2 = np.sqrt(np.diag(covariancePolynomT2))
#errorsB1T2 = np.sqrt(np.diag(covarianceBruch1T1))
#errorsB2T2 = np.sqrt(np.diag(covarianceBruch2T1))
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
"""
print('Bruch1approximation T1')
print('A =', paramsBruch1T1[0], 'pm', errorsB1T1[0])
print('B =', paramsBruch1T1[1], 'pm', errorsB1T1[1])
print('C =', paramsBruch1T1[2], 'pm', errorsB1T1[2])
print('Bruch1approximation T2')
print('A =', paramsBruch1T2[0], 'pm', errorsB1T2[0])
print('B =', paramsBruch1T2[1], 'pm', errorsB1T2[1])
print('C =', paramsBruch1T2[2], 'pm', errorsB1T2[2])
print('Bruch2approximation T1')
print('A =', paramsBruch2T1[0], 'pm', errorsB2T1[0])
print('B =', paramsBruch2T1[1], 'pm', errorsB2T1[1])
print('C =', paramsBruch2T1[2], 'pm', errorsB2T1[2])
print('D =', paramsBruch2T1[3], 'pm', errorsB2T1[3])
print('Bruch2approximation T2')
print('A =', paramsBruch2T2[0], 'pm', errorsB2T2[0])
print('B =', paramsBruch2T2[1], 'pm', errorsB2T2[1])
print('C =', paramsBruch2T2[2], 'pm', errorsB2T2[2])
print('D =', paramsBruch2T2[3], 'pm', errorsB2T2[3])
"""
plt.cla()
plt.clf()
#Graphenapproximation
x_plot = np.linspace(0, 18)
paramboundBruch2 = ([])
plt.plot(Zeitab, T1, 'rx', label ="Temparatur1")
plt.plot(x_plot, Polynom(x_plot, *paramsPolynomT1), 'b-', label='Fit durch Polynome', linewidth=3)
#plt.plot(x_plot, Bruch1(x_plot, *paramsBruch1T1), 'g-', label='Fit durch Bruch1', linewidth=3)
#plt.plot(x_plot, Bruch2(x_plot, *paramsBruch2T1), 'r-', label='Fit durch Bruch2', linewidth=3)
plt.legend(loc="best")
plt.savefig("Temparatur1.png")
plt.cla()
plt.clf()
plt.plot(Zeitab, T2, 'rx', label ="Temparatur2")
plt.plot(x_plot, Polynom(x_plot, *paramsPolynomT2), 'b-', label='Fit durch Polynome', linewidth=3)
#plt.plot(x_plot, Bruch1(x_plot, *paramsBruch1T2), 'g-', label='Fit durch Bruch1', linewidth=3)
#plt.plot(x_plot, Bruch2(x_plot, *paramsBruch2T2), 'r-', label='Fit durch Bruch2', linewidth=3)
plt.legend(loc="best")
plt.savefig("Temparatur2.png")


#Güte bestimmen
#Formel
A2T1 = 2*PolynomAT1
A2T2 = 2*PolynomAT2
print('koeffableitungAT1',A2T1)
print('koeffableitungAT2',A2T2)
def Ableitung(x, A, B):
    return A*x+B

def Massendurch(DeltaT2,Deltat,m2,mk,cw,ck,L):
    return (m1*cw+mk*ck)*DeltaT1/(Deltat*L)

def Liestung(k,Pb,Pa,roh):
    Deltm = Massendurch()
    return 1/(k-1)*(Pb*(Pa/Pb)**(1/k)-Pa)*1/roh*Deltm
print('Ableitung',Ableitung(12*60,A2T1,PolynomBT1))
def realGuete(Jim,m1,mkck,cw,N):
    return (m1*cw+mkck)*Jim/N

print('GueteT1bei 2',realGuete(Ableitung(2,A2T1,PolynomBT1),3,660,cWasser,Leistung[2]))
print('GueteT1bei 8',realGuete(Ableitung(8,A2T1,PolynomBT1),3,660,cWasser,Leistung[8]))
print('GueteT1bei 12',realGuete(Ableitung(12,A2T1,PolynomBT1),3,660,cWasser,Leistung[12]))
print('GueteT1bei 16',realGuete(Ableitung(16,A2T1,PolynomBT1),3,660,cWasser,Leistung[16]))

#ideal
print(T1[16]/(T1[16]-T2[16]))
#Rechnung
