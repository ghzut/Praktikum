import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt




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


x, y = np.genfromtxt('content/aufgabendatena.txt', unpack=True)
makeTable([x, y], [r'$\Delta t/\mu$s', r'$\Delta A/$V'], '', 'taba', ['4.0', '2.1'])



def f(x, a , b):
    return a / np.sqrt(1+x**2 * b**2)


x, y = np.genfromtxt('content/aufgabendatenb.txt', unpack=True)
makeTable([x, y], [r'$f/$Hz', r'$A/$V'], '', 'tabb', ['6.1', '2.3'])
namex, namey = [r'$f/$Hz', r'$A/$V']
params, covar = curve_fit(f , x, y)
plt.cla()
plt.clf()
t = np.linspace(x[0], x[-1], 100000)
print('b', params, covar, sep='\n')
plt.plot(x, y, 'rx', label='Daten')
plt.plot(t, f(t, *params), 'b-', label='Fit')
plt.xlim(x[0], x[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.xscale('log')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grab')

def f2(x, a):
    return np.arctan(-x*a)

x, y = np.genfromtxt('content/aufgabendatenc.txt', unpack=True)
makeTable([x, y], [r'$f/$Hz', r'$\Delta t/\mu$s'], '', 'tabc', [])
y = y*(10**(-6))*x*2*np.pi
x = 2 * np.pi *x
namex, namey = [r'$\omega/$s$^{-1}$', r'$\varphi$']
params2, covar = curve_fit(f2 , x[0:-5], y[0:-5])
plt.cla()
plt.clf()
t = np.linspace(x[0], x[-5], 100000)
print('c', params2, covar, sep='\n')
plt.plot(x, y, 'rx', label='Daten')
plt.plot(t, f2(t, *params2), 'b-', label='Fit')
plt.xlim(t[0], t[-1])
plt.xlabel(namex)
plt.ylabel(namey)
plt.xscale('log')
plt.legend(loc='best')
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/'+'grac')
