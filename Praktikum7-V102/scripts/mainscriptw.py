from table import makeTable
from bereich import bereich
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp


#Für alle#####################################

#kg Masse der Kugel
MK = unp.uarray(0.5122, 0.5122*0.04)
print('Masse der Kugel: ', MK)

#m Durchmesser der Kugel
DK = unp.uarray(50.76/(10**3), 50.76/(10**3) * 0.007) 
print('Durchmesser der Kugel: ', DK)

#m Radius der Kugel
RK = DK/2 
print('Radius der Kugel: ', RK)

#Trägheitsmoment der Kugel
TK = 2/5 * MK * RK **2
print('Trägheitsmoment der Kugel: ', TK)

#kg m^2 Trägheitsmoment der Kugelhalterung
TKh = (22.5/10**4)/10**3 
print('Trägheitsmoment der Kugelhalterung: ', TKh)

# Windungszahl der Spule Helmholzspule
WzH = 390 
print('Windungszahl der Helmholzspule: ', WzH)

#m Radius der Helmholzspule
RH = 78 / 10**3 
print('Radius der Helmholzspule: ', RH)

#Ampere Maximalstrom der Helmholzspule
MsH = 1.4 

#m Länge des Drahtes
LD = 58.5 / 10**2 
print('Länge des Drahtes: ', LD)

#m Durchmesser des Drahtes
DD = np.array([0.172, 0.172, 0.17, 0.175, 0.18, 0.165])/10**3
DD = unp.uarray(np.mean(DD), stats.sem(DD))
print('Durchmesser des Drahtes: ', DD)

#m Radius des Drahtes
RD = DD / 2
print('Radius des Drahtes: ', RD)

#s Periodendauer normal
T1 = np.genfromtxt('scripts/magnetachseIstFadenachse', unpack=True)
T1 = unp.uarray(np.mean(T1), stats.sem(T1))
print('Periodendauer normal: ', T1)

#s Periodendauer im Erdmagnetfeld
T2 = np.genfromtxt('scripts/magnetparalelzu erdfeld', unpack=True)
T2 = unp.uarray(np.mean(T2), stats.sem(T2))
print('Periodendauer im Erdmagnetfeld: ', T2)

#s Periodendauer in der Helmholzspule
T3 = np.genfromtxt('scripts/inderhelmholtzspule')
print('Periodendauer in der Helmholzspule: ')
print(T3)

#Pa Elastizitätsmodul
E = unp.uarray(210, 0.5) * 10**9
print('Elastizitätsmodul: ', E)

#Pa Schubmodul
G = 8 * np.pi * LD * (TK+TKh)/ (T1**2 * RD**4)
print('Schubmodul: ', G)





