import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def f(x, a, b):
    return a * x + b


def plot(x, y, namex, namey, name):
    plt.cla()
    plt.clf()
    t = np.linspace(x[0], x[-1], 1000)
    parameters, pcov = curve_fit(f, x, y)
    print(name, parameters, np.sqrt(np.diag(pcov)), sep='\n')
    plt.plot(x, y, 'rx', label='Daten')
    plt.plot(t, f(t, *parameters), 'b-', label='Fit')
    plt.xlim(t[0], t[-1])
    plt.xlabel(namex)
    plt.ylabel(r'$U/V$')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('build/'+name)
    data = (x, y)
    names = namex, namey
    formats = []
    makeTable(data, names, name, formats)


def makeTable(data, names, name, formats):
    TableFile = open('build/'+name+'.tex', 'w+')
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



y, x = np.genfromtxt('Gleichstrom', unpack=True)
plot(x, y, r'$I/mA$', r'$U/V$', 'Gleichstrom')

y, x = np.genfromtxt('GleichstromR', unpack=True)
plot(x, y, r'$I/mA$', r'$U/V$', 'GleichstromR')

y, x = np.genfromtxt('Aufgabed_Rechteckspannung.txt', unpack=True)
plot(x, y, r'$I/mA$', r'$U/V$', 'Rechteck')

y, x = np.genfromtxt('Aufgabed_Sinusspannung.txt', unpack=True)
plot(x, y, r'$I/mA$', r'$U/V$',  'Sinus')
