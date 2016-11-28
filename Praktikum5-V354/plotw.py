import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import uncertainties.unumpy as unp





def linregress(x, y):
    assert len(x) == len(y)

    x, y = np.array(x), np.array(y)

    N = len(y)
    Delta = N * np.sum(x**2) - (np.sum(x))**2

    A = (N * np.sum(x * y) - np.sum(x) * np.sum(y)) / Delta
    B = (np.sum(x**2) * np.sum(y) - np.sum(x) * np.sum(x * y)) / Delta

    sigma_y = np.sqrt(np.sum((y - A * x - B)**2) / (N - 2))

    A_error = sigma_y * np.sqrt(N / Delta)
    B_error = sigma_y * np.sqrt(np.sum(x**2) / Delta)

    return [A, B], [A_error, B_error, sigma_y]

def plot(x, y, namex, namey, name):
    plt.cla()
    plt.clf()
    t = np.linspace(x[0], x[-1], 1000)
    parameters, pcov = linregress(x, y)
    print(name, parameters, pcov, sep='\n')
    plt.plot(x, y, 'rx', label='Daten')
    plt.plot(t, f(t, *parameters), 'b-', label='Fit')
    plt.xlim(t[0], t[-1])
    plt.xlabel(namex)
    plt.ylabel(namey)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('build/'+name)
    data = (x, y)
    names = namex, namey
    formats = []
    makeTable(data, names, '', name, formats)

def makeTable(data, names, name, filename, formats):
    TableFile = open('build/'+filename+'.tex', 'w+')
    TableFile.write(r'\begin{table}'+'\n\t'+r'\centering'+'\n\t'+r'\caption{'+name+r'}'+'\n\t'+r'\label{tab:'+name+'}\n\t'+r'\sisetup{table-format=1.2}'+'\n\t'+r'\begin{tabular}{')
    for i in range(len(data)):
        if formats:
            TableFile.write(r'S[table-format='+formats[i]+'] ')
        else:
            TableFile.write('S ')
    TableFile.write('}\n\t\t')
    TableFile.write(r'\toprule'+'\n\t\t')
    for nam in names[0:-1]:
        TableFile.write('{'+nam+'} & ')

    TableFile.write('{'+names[-1]+'}'+r' \\'+'\n\t\t')
    TableFile.write(r'\midrule'+'\n\t\t')
    for i in range(len(data[0])):
        for value in data[0:-1]:
            TableFile.write(str(value[i]))
            TableFile.write(r' & ')
        TableFile.write(str(data[-1][i]))
        TableFile.write(r' \\')
        TableFile.write('\n\t\t')


    TableFile.write(r'\bottomrule'+'\n\t')
    TableFile.write(r'\end{tabular}'+'\n')
    TableFile.write(r'\end{table}')

def bereich(x, u, o):
	if(x>=u and x<=o):
		return x
	if(x<u):
		return bereich(o - (u-x), u, o)
	if(x>o):
		return bereich(u + (x-o), u, o)




#allesallesallesallesalles
C, Cf, L, Lf = np.genfromtxt('content/aufgabendatenb', unpack=True)
C = unp.uarray(C, Cf)*10**(-9)
L = unp.uarray(L, Lf)*10**(-3)
R1 = unp.uarray(67.2, 0.2)
R2 = unp.uarray(682, 1)


#aaaaaaaaaaaaaaaaaaaaaaaaa
print('a)')

def f(t, w, U):
	return U*np.exp(-w*t)

x, y = np.genfromtxt('content/aufgabendatena', unpack=True)
makeTable([x, y], [r'$\Delta t/\mu$s', r'$\Delta A/$V'], 'Messwerte zu Versuchsteil a)', 'taba', ['4.0', '2.1'])
namex, namey = [r'$\Delta t/\mu$s', r'$\Delta A/$V']
x = x * 10**(-6)
params, covar = curve_fit(f, x, y)
plt.cla()
plt.clf()
t = np.linspace(x[0], x[-1], 100000)
print(params, covar, sep='\n')
x = x * 10**6
plt.plot(x, y, 'rx', label='Daten')
t2 = t *10**6
plt.plot(t2, f(t, *params), 'b-', label='Fit')
plt.xlim(x[0], x[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'graa')
gamma = unp.uarray(params[0], np.sqrt(covar[0][0]))
U = unp.uarray(params[1], np.sqrt(covar[1][1]))
print('gamma = ', gamma)
print('U(0) = ', U)
#print('gammaerrechnet = ', R1/(2*L))
print('Reff = ', gamma*2*L)
print('R gegeben = ', R1)

#bbbbbbbbbbbbbbbbbbbb 
print('b)')

Rap = unp.sqrt(4 * L / C)

print('C = ', C, ', L = ', L, ', Rap = ', Rap)
print('Rap gemessen = ', 272)

#cccccccccccccccccccc
def AcT(f, LCs, RC):
	return 1/np.sqrt((1-(2*np.pi*f*LCs)**2)**2+(RC*2*np.pi*f)**2)
	

print('c)')
f, Ac, A = np.genfromtxt('content/aufgabendatenc', unpack=True)
RelativAmplitude = Ac/A
makeTable([f, Ac, A], [r'$f/$Hz', r'$A_C/$V', r'$A/$V'], 'Messwerte zu Versuchsteil c)', 'tabc', ['6.0', '2.3', '2.3'])
namex, namey  = [r'$f/$Hz', r'$A_C/A$']
f2 = f / 1000000
params, covar = curve_fit(AcT, f2, RelativAmplitude)
plt.cla()
plt.clf()
t = np.linspace(f[0], f[-1], 100000)
print(params, covar, sep='\n')
t2 = t / 1000000
plt.plot(f, RelativAmplitude, 'rx', label='Daten')
plt.plot(t, AcT(t2, *params), 'b-', label='Fit')
plt.xlim(f[0], f[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.xscale('log')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grac1')
LC = (unp.uarray(params[0], np.sqrt(covar[0][0]))/1000000)**2
RC = unp.uarray(params[1], np.sqrt(covar[1][1]))/1000000
print('LC = ', LC)
print('RC = ', RC)
print('LC errechnet = ', L*C)
print('RC errechnet = ', R2*C)


q = unp.sqrt(LC)/RC
print('Güte q = ', q)
qer = unp.sqrt(L*C)/(R2*C)
print('Güte q errechnet = ', qer)







a = (RC**2-2*LC)/(2*LC**2)
print('a = ', a)
w1 = unp.sqrt(-a - unp.sqrt(a**2 - (1-2/q**2)/LC**2))
w2 = unp.sqrt(-a + unp.sqrt(a**2 - (1-2/q**2)/LC**2))
print('w- = ', w1)
print('w+ = ', w2)
print('f- = ', w1 / (2*np.pi))
print('f+ = ', w2 / (2*np.pi))
print('Breite der Ressonanzkurve = ', (w2 - w1) / (2*np.pi))

aer = ((R2*C)**2-2*L*C)/(2*(L*C)**2)
print('a errechnet = ', aer)
w1er = unp.sqrt(-aer - unp.sqrt(aer**2 - (1-2/qer**2)/(L*C)**2))
w2er = unp.sqrt(-aer + unp.sqrt(aer**2 - (1-2/qer**2)/(L*C)**2))
print('w- errechnet = ', w1er)
print('w+ errechnet = ', w2er)
print('f- errechnet = ', w1er / (2*np.pi))
print('f+ errechnet = ', w2er / (2*np.pi))
print('Breite der Ressonanzkurve errechnet = ', (w2er - w1er) / (2*np.pi))


fplus = unp.nominal_values(w2)/(2*np.pi)
fplus2 = fplus / 1000000
fminus = unp.nominal_values(w1)/(2*np.pi)
fminus2 = fminus / 1000000

f2 = f[10:-5]
RelativAmplitude2 = RelativAmplitude[10:-5]

plt.cla()
plt.clf()
t = np.linspace(f2[0], f2[-1], 100000)
t2 = t / 1000000
#print(params, covar, sep='\n')
plt.plot(f2, RelativAmplitude2, 'rx', label='Daten')
plt.plot(t, AcT(t2, *params), 'b-', label='Fit')
plt.xlim(f2[0], f2[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grac2')

#dddddddddddddddddddddddddddddddd
print('d)')

def f3(a, LCs, RC):
	b = []
	for x in a:
		b.append(bereich(np.arctan((2*np.pi*x*RC)/(1-(LCs*2*np.pi*x)**2)), 0, np.pi))
	return np.array(b)


x2, z2 = np.genfromtxt('content/aufgabendatend', unpack=True)

makeTable([x2, z2], [r'$f/$Hz', r'$\Delta t/\mu$s'], 'Messwerte zu Versuchsteil d)', 'tabd', ['6.1', '3'])
z2 = z2*(10**(-6))*x2*2*np.pi
#b = []
#for z in z2:
#	b.append(bereich(z, -np.pi/2, np.pi/2))
	#print('Zahl = ', z, ' ', bereich(z, -np.pi/2, np.pi/2))
#z2 = np.array(b)
namex, namey = [r'$f/$Hz', r'$\varphi$']
#p0=[np.sqrt(3.6*10**(-11))*10**6, 1.5]
params2, covar = curve_fit(f3 , x2/1000000, z2, p0=[np.sqrt(3.6*10**(-11))*10**6, 1.5])
plt.cla()
plt.clf()
t = np.linspace(x2[0], x2[-1], 100000)
t2 = t / 1000000
print(params2, covar, sep='\n')
plt.plot(x2, z2, 'rx', label='Daten')
plt.plot(t, f3(t2, *params2), 'b-', label='Fit')
plt.xlim(t[0], t[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.xscale('log')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grad1')
LC = (unp.uarray(params[0], np.sqrt(covar[0][0]))/1000000)**2
RC = unp.uarray(params[1], np.sqrt(covar[1][1]))/1000000
print('LC = ', LC)
print('RC = ', RC)
print('fres = ', unp.sqrt(1/(LC) - (RC**2)/(2*LC**2))/(2*np.pi) )
print('fres errechnet = ', unp.sqrt(1/(L*C) - (R2**2)/(2*L**2))/(2*np.pi) )
print('f1 = ', (RC/(2*LC) + unp.sqrt(RC**2/(2*LC)**2 + 1/LC))/(2*np.pi) )
print('f1 errechnet = ', (R2/(2*L) + unp.sqrt(R2**2/(2*L)**2 + 1/(L*C)))/(2*np.pi) )
print('f2 = ', (-RC/(2*LC) + unp.sqrt(RC**2/(2*LC)**2 + 1/LC))/(2*np.pi) )
print('f2 errechnet = ', (-R2/(2*L) + unp.sqrt(R2**2/(2*L)**2 + 1/(L*C)))/(2*np.pi) )


plt.cla()
plt.clf()
t = np.linspace(x2[0], x2[-1], 100000)
t2 = t / 1000000
plt.plot(x2, z2, 'rx', label='Daten')
plt.plot(t, f3(t2, *params2), 'b-', label='Fit')
plt.xlim(x2[5], t[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grad2')






