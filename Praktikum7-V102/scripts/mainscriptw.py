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
print('Masse der Kugel: ', MK, 'kg')

#m Durchmesser der Kugel
DK = unp.uarray(50.76/(10**3), 50.76/(10**3) * 0.007) 
print('Durchmesser der Kugel: ', DK, 'm')

#m Radius der Kugel
RK = DK/2 
print('Radius der Kugel: ', RK, 'm')

#kg m^2 Trägheitsmoment der Kugel
TK = 2/5 * MK * RK **2
print('Trägheitsmoment der Kugel: ', TK, 'kg*m^2')

#kg m^2 Trägheitsmoment der Kugelhalterung
TKh = (22.5/10**4)/10**3 
print('Trägheitsmoment der Kugelhalterung: ', TKh, 'kg*m^2')

# Windungszahl der Spule Helmholzspule
WzH = 390 
print('Windungszahl der Helmholzspule: ', WzH)

#m Radius der Helmholzspule
RH = 78 / 10**3 
print('Radius der Helmholzspule: ', RH, 'm')

#Ampere Maximalstrom der Helmholzspule
MsH = 1.4 

#m Länge des Drahtes
LD = 58.5 / 10**2 
print('Länge des Drahtes: ', LD, 'm')

#m Durchmesser des Drahtes
DD = np.array([0.172, 0.172, 0.17, 0.175, 0.18, 0.165])/10**3
DD = unp.uarray(np.mean(DD), stats.sem(DD))
print('Durchmesser des Drahtes: ', DD, 'm')

#m Radius des Drahtes
RD = DD / 2
print('Radius des Drahtes: ', RD, 'm')

#s Periodendauer normal
T1 = np.genfromtxt('scripts/magnetachseIstFadenachse', unpack=True)
T1 = unp.uarray(np.mean(T1), stats.sem(T1))
print('Periodendauer normal: ', T1, 's')

#s Periodendauer im Erdmagnetfeld
T2 = np.genfromtxt('scripts/magnetparalelzu erdfeld', unpack=True)
T2 = unp.uarray(np.mean(T2), stats.sem(T2))
print('Periodendauer im Erdmagnetfeld: ', T2, 's')

#s Periodendauer in der Helmholzspule 
T3 = np.genfromtxt('scripts/inderhelmholtzspule')
T3t = []
for line in T3:
	T3t.append(unp.uarray(np.mean(line), stats.sem(line)))

T3 = np.array(T3t)
print('Periodendauer in der Helmholzspule: ')
i = 1
I = []
for line in T3:
	print('Bei ', i/10, ' Ampere: ',  line, ' T', sep='')
	I.append(i/10)
	i += 1

#A Stromstärke
I = np.array(I)


#T Magnetfeldstärke
B = 4 * np.pi * 10**(-7) * 8 * I * WzH / (RH * np.sqrt(125))
print('Magnetfeldstärken: ', B, 'T')

#Pa Elastizitätsmodul
E = unp.uarray(210, 0.5) * 10**9
print('Elastizitätsmodul: ', E, 'Pa')

#Pa Schubmodul
G = 8 * np.pi * LD * (TK+TKh)/ (T1**2 * RD**4)
print('Schubmodul: ', G, 'Pa')

# Poissonsche Querkontraktionszahl
mu = E / (2*G) - 1
print('Querkontraktionszahl: ', mu)

#Pa Kompressionsmodul
Q = E / (3*(1-2*mu))
print('Kompressionsmodul: ', Q, 'Pa')


#plotsplotsplotsplotsplotsplotsplots
def line(x, a, b):
	return a * x + b
dT3s = 1/T3**2
dT3sn = []
dT3sstd = []
for value in dT3s:
	dT3sn.append(unp.nominal_values(value))
	dT3sstd.append(unp.std_devs(value))

dT3sn = np.array(dT3sn)
dT3sstd = np.array(dT3sstd)

namex, namey = [r'$T^{-2}/\si{\per\second\squared}$', r'$B/\si{\tesla}$']
t = np.linspace(dT3sn[0]-dT3sn[-1]*0.02 , dT3sn[-1]*1.02 , 10000)
params, covar = curve_fit(line, dT3sn, B)
plt.cla()
plt.clf()
plt.figure()
plt.plot(dT3sn, B, 'rx', label='Daten')
plt.plot(t, line(t, *params), 'b-', label='Fit')
plt.xlim(t[0], t[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'helmholzspule')

#Am^2 magnetisches Moment
m = unp.uarray(params[0], np.sqrt(covar[0][0]))
print('magnetisches Moment: ', m, 'A*m^2')


#T Erdmagnetfeld
BE = line(1/T2**2, m, unp.uarray(params[1], np.sqrt(covar[1][1])))
print('Erdmagnetfeldstärke: ', BE, 'T')



#namex, namey = [r'Gliednummer', r'$U_3/\si{\milli\volt}$']
#t = np.linspace(0, 14, 100000)
#plt.cla()
#plt.clf()
#plt.plot(x, U3, 'rx', label='Daten')
#plt.plot(t, line(t, 0, 24), 'b-', label='Fit')
#plt.xlabel(namex)
#plt.ylabel(namey)
#plt.legend(loc='best')
#plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
#plt.savefig('build/'+'grad3')

#makeTable([x, U1, U2, U3], [r'Gliednummer', r'$U_{1}/\si{\volt}$', r'$U_{2}/\si{\volt}$', r'$U_{3}/\si{\milli\volt}$'], 'Messwerte zu Versuchsteil d) und e).', 'tabd', ['2', '2.1', '1.2', '2.1'])



