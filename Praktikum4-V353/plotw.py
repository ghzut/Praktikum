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


#aaaaaaaaaaaaaaaaaaaaaaaaa

def f(x, a, b):
	return a*x+b

x, y = np.genfromtxt('content/aufgabendatena.txt', unpack=True)
makeTable([x, y], [r'$\Delta t/\mu$s', r'$U_C/$V'], 'Messwerte zu Versuchsteil a)', 'taba', ['4.0', '2.1'])
namex, namey = [r'$\Delta t/\mu$s', r'$U_C/$V']
params, var = linregress(x, np.log(y))
plt.cla()
plt.clf()
t = np.linspace(x[0], x[-1], 100000)
print('a', params, var, sep='\n')
plt.plot(x, y, 'rx', label='Daten')
plt.plot(t, np.exp(f(t, *params)), 'b-', label='Fit')
plt.xlim(x[0], x[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.yscale('log')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'graa')
Unulla = unp.exp(unp.uarray(params[1], var[1]))
RCa = -1/ (unp.uarray(params[0], var[0]) * 10 ** 6)
print('U_0 = ', Unulla)
print('RC = ', RCa)

#bbbbbbbbbbbbbbbbbbbb

def f2(x, a , b):
    return a / np.sqrt(1+(x*2*np.pi)**2 * b**2)


x, y, z = np.genfromtxt('content/aufgabendatenb.txt', unpack=True, missing_values='NA')
makeTable([x, y], [r'$f/$Hz', r'$A/$V'], 'Messwerte zu Versuchsteil b)', 'tabb', ['6.1', '2.3'])
namex, namey = [r'$f/$Hz', r'$A/$V']
params, covar = curve_fit(f2 , x, y)
plt.cla()
plt.clf()
t = np.linspace(x[0], x[-1], 100000)
print('b', params, covar, sep='\n')
plt.plot(x, y, 'rx', label='Daten')
plt.plot(t, f2(t, *params), 'b-', label='Fit')
plt.xlim(x[0], x[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.xscale('log')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grab')
Unullb = unp.uarray(params[0], np.sqrt(covar[0][0]))
Unullb2 = params[0]
RCb = -unp.uarray(params[1], np.sqrt(covar[1][1]))
print('U_0 = ', Unullb)
print('RC = ', RCb)


indeces = []
a = 0
for element in z:
    if np.isnan(element):
        indeces.append(a)
    a = a + 1


#x, y, z = np.genfromtxt('content/aufgabendatenb.txt', unpack=True, missing_values='NA')
#print(z)
#print(indeces)
#print(z)
x2 = np.delete(x, indeces)
y2 = np.delete(y, indeces)
z2 = np.delete(z, indeces)
#print(z2)
#dddddddddddddd
makeTable([x2, y2, z2], [r'$f/$Hz', r'$A/$V', r'$\Delta t/\mu$s'], 'Messwerte zu Versuchsteil d)', 'tabd', ['6.1', '2.3', '3'])
def f4(x):
	return np.sin(x)*np.sqrt(1/(np.sin(x)**2)-1)


z2 = z2*(10**(-6))*x2*2*np.pi
p = np.linspace(0, np.pi/2, 1000)
p = p[1:-1]
#print(p)
plt.cla()
plt.clf()
plt.polar(p, f4(p))
plt.polar(z2, y2/(Unullb2), 'rx')
plt.savefig('build/'+'grad')
#disdisdisdisdisdis

def f3(x, a):
    return np.arctan(-2*np.pi*x*a)

x2, z2 = np.genfromtxt('content/aufgabendatenc.txt', unpack=True)
#makeTable([x2, z2], [r'$f/$Hz', r'$\Delta t/\mu$s'], '', 'tabdis', ['6.1', '3'])
z2 = z2*(10**(-6))*x2*2*np.pi
namex, namey = [r'$f/$Hz', r'$\varphi$']
params2, covar = curve_fit(f3 , x2, z2)
plt.cla()
plt.clf()
t = np.linspace(x2[0], x2[-1], 100000)
print('dis', params2, covar, sep='\n')
plt.plot(x2, z2, 'rx', label='Daten')
plt.plot(t, f3(t, *params2), 'b-', label='Fit')
plt.xlim(t[0], t[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.xscale('log')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'gradis')
RCc = unp.uarray(-params2[0], np.sqrt(covar[0][0]))
print('RC = ', RCc)


#ccccccccccccccccccc



x2, z2 = np.genfromtxt('content/aufgabendatencalt.txt', unpack=True)
makeTable([x2, z2], [r'$f/$Hz', r'$\Delta t/\mu$s'], 'Messwerte zu Versuchsteil c)', 'tabc', ['6.1', '3'])
z2 = z2*(10**(-6))*x2*2*np.pi
namex, namey = [r'$f/$Hz', r'$\varphi$']
params2, covar = curve_fit(f3 , x2[0:-4], z2[0:-4])
plt.cla()
plt.clf()
t = np.linspace(x2[0], x2[-1], 100000)
print('c', params2, covar, sep='\n')
plt.plot(x2, z2, 'rx', label='Daten')
plt.plot(t, f3(t, *params2), 'b-', label='Fit')
plt.xlim(t[0], t[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.xscale('log')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grac')
RCc = unp.uarray(-params2[0], np.sqrt(covar[0][0]))
print('RC = ', RCc)


