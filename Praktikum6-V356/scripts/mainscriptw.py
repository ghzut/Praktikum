
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp


















#nichts


def f(t, w, U):
	return U*np.exp(-w*t)

#x, y = np.genfromtxt('content/aufgabendatena', unpack=True)
#makeTable([x, y], [r'$\Delta t/\si{\micro\second}$', r'$A_C/\si{\milli\volt}$'], 'Messwerte zu Versuchsteil a).', 'taba', ['3.1', '3.1'])
namex, namey = [r'$\Delta t/\si{\micro\second}$', r'$A_C/\si{\milli\volt}$']
#params, covar = curve_fit(f, x, y)
plt.cla()
plt.clf()
t = np.linspace(0, 10000, 100000)
#print(params, covar, sep='\n')
#plt.plot(x, y, 'rx', label='Daten')
plt.plot(t, f(t, 1, 1), 'b-', label='Fit')
#plt.xlim(x[0], x[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'graa')
#gamma = unp.uarray(params[0], np.sqrt(covar[0][0]))
#U = unp.uarray(params[1], np.sqrt(covar[1][1]))


#allesallesallesallesalles
L = 1
C1 = 1
C2 = 1

#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
print('a)')
print('gf1 = ', np.sqrt(2/(L*C1)))
print('gf2 = ', np.sqrt(2/(L*C2)))
print('gf3 = ', np.sqrt(2*(C1+C2)/(L*C1*C2)))

#bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
print('b)')

def w2(theta, L, C1, C2):
	return np.sqrt(1/L * (1/C1 + 1/C2) - 1/L * np.sqrt((1/C1 + 1/C2)**2 - 4*np.sin(theta)**2 / (C1*C2)))

def w1(theta, L, C1, C2):
	return np.sqrt(1/L * (1/C1 + 1/C2) + 1/L * np.sqrt((1/C1 + 1/C2)**2 - 4*np.sin(theta)**2 / (C1*C2)))

def w(theta, L, C):
	return np.sqrt(2/(L*C) * (1-np.cos(theta)))


f = genfromtxt('datenb', unpack = True)

namex, namey = [r'$\theta$', r'$\omega/\si{\per\second}$']
t = np.linspace(0, np.pi/2, 100000)
plt.cla()
plt.clf()
plt.plot(t, w(t, L, 2*C1), 'y-', label='Theorie w')
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grab1')
plt.cla()
plt.clf()
plt.plot(t, w2(t, L, C1, C2), 'b-', label='Theorie w2')
plt.plot(t, w1(t, L, C1, C2), 'r-', label='Theorie w1')
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grab2')




	


