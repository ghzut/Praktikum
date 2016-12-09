from table import makeTable
from bereich import bereich
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp


#Für alle#####################################

#kg Masse der Kugel
MK = unp.uarray(0.5122, 0.5122*0.04)

#m Durchmesser der Kugel
DK = unp.uarray(50.76/(10**3), 50.76/(10**3) * 0.007) 

#m Radius der Kugel
RK = DK/2 

#kg m^2 Trägheitsmoment der Kugelhalterung
TKh = (22.5/10**4)/10**3 

# Windungszahl der Spule Helmholzspule
WzH = 390 

#m Radius der Helmholzspule
RH = 78 / 10**3 

#Ampere Maximalstrom der Helmholzspule
MsH = 1.4 

#m Länge des Drahtes
LD = 58.5 / 10**2 

#m Dicke des Drahtes
DnD = np.array([0.172, 0.172, 0.17, 0.175, 0.18, 0.165])/10**3 

#s Periodendauer normal
T1 = np.genfromtxt('scripts/magnetachseIstFadenachse', unpack=True)

#s Periodendauer im Erdmagnetfeld
T2 = np.genfromtxt('scripts/magnetparalelzu erdfeld', unpack=True)

#s Periodendauer in der Helmholzspule
T3 = np.genfromtxt('scripts/inderhelmholtzspule')


#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
print(T1)
print(T2)
print(T3)

