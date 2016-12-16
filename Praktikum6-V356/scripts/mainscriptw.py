from table import makeTable
from bereich import bereich
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp

#unnötig
def line(x,a,b):
	return a*x + b
x, y = np.genfromtxt('scripts/datenaLC', unpack=True)
y2 = np.genfromtxt('scripts/datenaLC1C2', unpack=True)

x1 = np.array([2, 4, 6, 8, 10 ,12, 14, 16, 18, 21, 23, 25])
x2 = np.array([2, 4, 6, 8, 11, 14, 17, 21, 24])

params, covar = curve_fit(line, x1, np.log(y))
print(params, covar, sep='\n')
t = np.linspace(0, 25, 100000)
plt.cla()
plt.clf()
plt.plot(x1, y, 'rx', label='Daten')
plt.plot(t, np.exp(line(t, *params)), 'b-', label='Fit')
#plt.xlim()
plt.xlabel('Kästchenanzahl')
plt.ylabel('$f/\si{\hertz}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'gramist1')

params, covar = curve_fit(line, x2, np.log(y2))
print(params, covar, sep='\n')
t = np.linspace(0, 25, 100000)
plt.cla()
plt.clf()
plt.plot(x2, y2, 'rx', label='Daten')
plt.plot(t, np.exp(line(t, *params)), 'b-', label='Fit')
#plt.xlim()
plt.xlabel('Kästchenanzahl')
plt.ylabel('$f/\si{\hertz}$')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'gramist2')










#nichts


#def f(t, w, U):
#	return U*np.exp(-w*t)

#x, y = np.genfromtxt('content/aufgabendatena', unpack=True)
#makeTable([x, y], [r'$\Delta t/\si{\micro\second}$', r'$A_C/\si{\milli\volt}$'], 'Messwerte zu Versuchsteil a).', 'taba', ['3.1', '3.1'])
#namex, namey = [r'$\Delta t/\si{\micro\second}$', r'$A_C/\si{\milli\volt}$']
#params, covar = curve_fit(f, x, y)
#plt.cla()
#plt.clf()
#t = np.linspace(0, 10000, 100000)
#print(params, covar, sep='\n')
#plt.plot(x, y, 'rx', label='Daten')
#plt.plot(t, f(t, 1, 1), 'b-', label='Fit')
#plt.xlim(x[0], x[-1])
#plt.xlabel(namex)
#plt.ylabel(namey)
#plt.legend(loc='best')
#plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
#plt.savefig('build/'+'graa')
#gamma = unp.uarray(params[0], np.sqrt(covar[0][0]))
#U = unp.uarray(params[1], np.sqrt(covar[1][1]))


#allesallesallesallesalles
L = 1.75 *10**(-3)
C1 = 22.0 *10**(-9)
C2 = 9.39 *10**(-9)
#C2 = 10.00 *10**(-9) #geänderter theoretischer wert

#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
print('a)')
print('gf1 = ', np.sqrt(2/(L*C1))/(2*np.pi))
print('gf2 = ', np.sqrt(2/(L*C2))/(2*np.pi))
print('gf3 = ', np.sqrt(2*(C1+C2)/(L*C1*C2))/(2*np.pi))
print('gf4 = ', np.sqrt(4/(L*C1))/(2*np.pi))


#bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
print('b)')

def w2(theta, L, C1, C2):
	return np.sqrt(1/L * (1/C1 + 1/C2) - 1/L * np.sqrt((1/C1 + 1/C2)**2 - 4*np.sin(theta)**2 / (C1*C2)))

def w1(theta, L, C1, C2):
	return np.sqrt(1/L * (1/C1 + 1/C2) + 1/L * np.sqrt((1/C1 + 1/C2)**2 - 4*np.sin(theta)**2 / (C1*C2)))

def w(theta, L, C):
	return np.sqrt((2/(L*C)) * (1-np.cos(theta)))


f1 = np.genfromtxt('scripts/datenbC', unpack = True)
f2 = np.genfromtxt('scripts/datenbC1C2', unpack = True)

N = 16;
theta1 = []
for n in range(len(f1)):
	theta1.append(np.pi*(n+1)/N)
theta1 = np.array(theta1)
#print(theta1)

f3 = f2[8:]
f2 = f2[0:8]
N = 16;
theta2 = []
for n in range(len(f2)):
	theta2.append(np.pi*n/(N))
theta2 = np.array(theta2)
#print(theta2)
N = 16;
theta3 = []
for n in range(len(f3)):
	theta3.append(np.pi*(len(f3)+3-n)/(N))
theta3 = np.array(theta3)
#print(theta3)



namex, namey = [r'$\theta$', r'$f/\si[per-mode=reciprocal]{\kilo\hertz}$']
t = np.linspace(0, 2*np.pi, 100000)
plt.cla()
plt.clf()
plt.plot(theta1, f1/1000, 'rx', label='Daten')
plt.plot(t, (w(t, L, C1)/(2*np.pi)) / 1000, 'b-', label='Theoriekurve')
plt.xlim(0, theta1[-1]+theta1[-1]*0.02)
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grab1')


plt.cla()
plt.clf()
plt.plot(theta2, f2/1000, 'rx', label='Daten')
plt.plot(theta3, f3/1000, 'rx')
plt.plot(t, (w2(t, L, C1, C2)/(2*np.pi))/1000, 'b-', label='Theoriekurve')
plt.plot(t, (w1(t, L, C1, C2)/(2*np.pi))/1000, 'b-')
plt.xlim(0, theta2[-1]+theta2[-1]*0.02)
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grab2')


a = np.mean(((f2-w2(theta2, L, C1, C2)/(2*np.pi))[1:]/(w2(theta2, L, C1, C2)/(2*np.pi))[1:]))
b = np.mean((f3-w1(theta3, L, C1, C2)/(2*np.pi))/(w1(theta3, L, C1, C2)/(2*np.pi)))
print(a)
print(b)
print(np.mean([a,b,0]))


makeTable([f1, np.around(theta1, decimals=2)], [r'$f/\si[per-mode=reciprocal]{\hertz}$', r'$\theta$'], r'Messwerte zu Versuchsteil b) mit $LC$-Kette mit zugehöriger Phasenverschiebung.', 'tabb1', ['5.1', '1.2'])
makeTable([np.append(f2, f3), np.around(np.append(theta2, theta3), decimals=2)], [r'$f/\si[per-mode=reciprocal]{\hertz}$', r'$\theta$'], r'Messwerte zu Versuchsteil b) mit $LC_1C_2$-Kette mit zugehöriger Phasenverschiebung.', 'tabb2', ['5.1', '1.2'])
t2 = np.array(range(len(f1))) + 1



#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
print('c)')

def vph(omega, L, C):
	return omega / np.arccos(1 - 1/2 * omega**2 * L * C)


f1 = np.genfromtxt('scripts/datencUnsere', unpack = True)
t2 = np.append(t2[0:-3],t2[-2:])
#print(t2)
theta1 = np.append(theta1[0:-3],theta1[-2:])

namex, namey = [r'$f/\si[per-mode=reciprocal]{\kilo\hertz}$', r'$v_{ph}/\frac{\si{\kilo\hertz}}{\text{rad}}$']
t = np.linspace(0, 2/(np.sqrt(L*C1)), 100000)
t = t[1:-1]
plt.cla()
plt.clf()
plt.plot(f1/1000, (f1*(2*np.pi)/theta1)/1000, 'rx', label='Daten')
plt.plot((t/(2*np.pi))/1000, vph(t, L, C1)/1000, 'b-', label='Theoriekurve')
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grac')
#n = 0
#for f in f1:
#	if n == 0:
#		print('Grundschwingung bei: ', f, ' Hz', sep='')
#	else:
#		print(n, '-te Oberschwingung bei: ', f, ' Hz' , sep='')
#	n = n+1


 
makeTable([t2, f1, np.around(theta1, decimals=2)], [r'Eigenschwingungsnummer', r'$f/\si[per-mode=reciprocal]{\hertz}$', r'$\theta$'], r'Messwerte zu Versuchsteil c) mit zugehöriger Phasenverschiebung bei verschiedenen Eigenschwingungen.', 'tabc', ['2', '5.1', '1.2'])


#ddddddddddddddddddddddddddddddddddddddddddddddddddddd
def cosinusbetragG(x, A):
	return A*np.sqrt(np.cos(np.pi/14 *x)**2)

def cosinusbetragO(x, A):
	return A*np.sqrt(np.cos(2*np.pi/14 *x)**2)


U1, U2, U3 = np.genfromtxt('scripts/datend', unpack = True)
U1 = U1 / 10
x = []
for n in range(len(U1)):
	x.append(n)
x = np.array(x)

params, covar = curve_fit(cosinusbetragG, x, U1, p0=[1.6])
print(params, covar, sep='\n')
namex, namey = [r'Gliednummer', r'$U_1/\si{\volt}$']
t = np.linspace(-0.2, 14.2, 100000)
plt.cla()
plt.clf()
plt.plot(x, U1, 'rx', label='Daten')
plt.plot(t, cosinusbetragG(t, *params), 'b-', label='Fit')
plt.xlim(t[0], t[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grad1')

params, covar = curve_fit(cosinusbetragO, x, U2, p0=[0.7])
print(params, covar, sep='\n')
namex, namey = [r'Gliednummer', r'$U_2/\si{\volt}$']
t = np.linspace(-0.2, 14.2, 100000)
plt.cla()
plt.clf()
plt.plot(x, U2, 'rx', label='Daten')
plt.plot(t, cosinusbetragO(t, *params), 'b-', label='Fit')
plt.xlim(t[0], t[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grad2')

def line(x, a, b):
	return a*x + b

namex, namey = [r'Gliednummer', r'$U_3/\si{\milli\volt}$']
t = np.linspace(-0.2, 14.2, 100000)
plt.cla()
plt.clf()
plt.plot(x, U3, 'rx', label='Daten')
plt.plot(t, line(t, 0, 24), 'b-', label='Fit')
plt.xlim(t[0], t[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grad3')

makeTable([x, U1, U2, U3], [r'Gliednummer', r'$U_{1}/\si{\volt}$', r'$U_{2}/\si{\volt}$', r'$U_{3}/\si{\milli\volt}$'], 'Messwerte zu Versuchsteil d) und e).', 'tabd', ['2', '2.1', '1.2', '2.1'])


	


