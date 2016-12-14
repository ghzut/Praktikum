from table import makeTable
from bereich import bereich
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp


#Für alle#####################################
namex = r'$x/\si{\centi\meter}$'
namey = r'$D(x)/\si{\milli\meter}$'

#eineitig eingespannt#########################

#RUNDSTAB#####################################
Ir = np.pi/4 * (0.005)**4
F = 9.81 * 0.7415

def DurchbiegungEinseitig1(x, a):
	return a*(0.52*x**2-(x**3)/3)

x, y1, y2 = np.genfromtxt('scripts/rundstab', unpack=True)
x = x/100
yd = (y1-y2)/1000**2
params, covar = curve_fit(DurchbiegungEinseitig1, x, yd, maxfev=1000)
print(params)
print(covar)
t = np.linspace(0, x[-1], 500)
plt.cla()
plt.clf()
plt.plot(x*100, yd*1000, 'rx', label='Daten')
plt.plot(t*100, DurchbiegungEinseitig1(t, *params)*1000, 'b-', label='Fit')
plt.xlim(t[0]*100, t[-1]*102)
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'rundstab')
a = unp.uarray(params[0], np.sqrt(covar[0][0]))
E = F/(2*a*Ir)
print('E1 =', E)

#QUARDRATSTAB#################################
Iq = 1/12 * 0.01**4
F = 9.81 * 1.2123

def DurchbiegungEinseitig2(x, a):
	return a*(0.5*x**2-(x**3)/3)

x, y1, y2 = np.genfromtxt('scripts/quadratstabeinseitig', unpack=True)
x = x/100
yd = (y1-y2)/1000**2
params, covar = curve_fit(DurchbiegungEinseitig2, x, yd, maxfev=1000)
print(params)
print(covar)
t = np.linspace(0, x[-1], 500)
plt.cla()
plt.clf()
plt.plot(x*100, yd*1000, 'rx', label='Daten')
plt.plot(t*100, DurchbiegungEinseitig2(t, *params)*1000, 'b-', label='Fit')
plt.xlim(t[0]*100, t[-1]*102)
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'quadratstabeinseitig')
a = unp.uarray(params[0], np.sqrt(covar[0][0]))
E = F/(2*a*Iq)
print('E2 =', E)


#QUARDRATSTABBEIDSEITIG########################
F = 9.81 * 3.5313

def DurchbiegungBeidseitig(x, a):
	links = a*(3*0.555**2*x[x<0.555/2]-4*(x[x<0.555/2]**3))
	rechts = a*(4*x[x>=0.555/2]**3 -12* 0.555* x[x>=0.555/2]**2 + 9 * 0.555**2 * x[x>=0.555/2] -0.555**3 )
	return np.append(links, rechts)



x, y1, y2 = np.genfromtxt('scripts/quadratstabbeidseitig', unpack=True)
x = x/100
yd = (y1-y2)/1000**2
params, covar = curve_fit(DurchbiegungBeidseitig, x, yd, maxfev=1000)
print(params)
print(covar)
t = np.linspace(0, 0.555, 500)
plt.cla()
plt.clf()
plt.plot(x*100, yd*1000, 'rx', label='Daten')
plt.plot(t*100, DurchbiegungBeidseitig(t, *params)*1000, 'b-', label='Fit')
plt.xlim(t[0]*100, t[-1]*100)
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'quadratstabbeidseitig')
a = unp.uarray(params[0], np.sqrt(covar[0][0]))
E = F/(48*a*Iq)
print('E3 =', E)



#T2 = unp.uarray(np.mean(T2), stats.sem(T2))




#makeTable([I,T3a[:, 0], T3a[:, 1], T3a[:, 2], T3a[:, 3], T3a[:, 4], np.around(T3n, decimals=3), np.around(T3nn, decimals=3), np.around(B*1000, decimals=3)], r'{$I/\si{\ampere}$} & {$T_1/\si{\second}$} & {$T_2/\si{\second}$} & {$T_3/\si{\second}$} & {$T_4/\si{\second}$} & {$T_5/\si{\second}$} & \multicolumn{2}{c}{$T_\text{m}/\si{\second}$} & {$B/\si{\milli\tesla}$}' , r'Die gemessenen Periodendauern der Schwingung unter Einwirkung des Magnetfeldes der Helmholzspule bei verschiedenen Stromstärken und die geschätzten Mittelwerte der Periodendauern $T_\text{m}$ sowie die zugehörigen magnetischen Flussdichten.', 'tabh', ['S[table-format=1.1]', r'S[table-format=2.3]', r'S[table-format=2.3]', r'S[table-format=2.3]', r'S[table-format=2.3]', r'S[table-format=2.3]', r'S[table-format=2.3]', r'@{${}\pm{}$} S[table-format=1.3]', r'S[table-format=1.3]'])








#dT3s = 1/T3**2
#dT3sn = []
#dT3sstd = []
#for value in dT3s:
#	dT3sn.append(unp.nominal_values(value))
#	dT3sstd.append(unp.std_devs(value))

#dT3sn = np.array(dT3sn)
#dT3sstd = np.array(dT3sstd)


#t = np.linspace(dT3sn[0]-dT3sn[-1]*0.02 , dT3sn[-1]*1.02 , 10000)
#params, covar = curve_fit(line, B, dT3sn, sigma=dT3sstd)
#a = unp.uarray(params[0], np.sqrt(covar[0][0]))
#b = unp.uarray(params[1], np.sqrt(covar[1][1]))
#plt.cla()
#plt.clf()
#plt.figure()
#plt.plot(dT3sn, B, 'rx', label='Daten')
#plt.plot(t, line(t, unp.nominal_values(a), unp.nominal_values(b)), 'b-', label='Fit')
#plt.xlim(t[0], t[-1])
#plt.xlabel(namex)
#plt.ylabel(namey)
#plt.legend(loc='best')
#plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
#plt.savefig('build/'+'helmholzspule')



