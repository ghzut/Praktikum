import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Datenfile erzeugen
def f(x, a, b):
    return a * x + b

def plot(x, y, name):
    plt.cla()
    plt.clf()
    t = np.linspace(x[0], x[-1], 1000)
    parameters, pcov = curve_fit(f, x, y)
    print(parameters, np.sqrt(np.diag(pcov)), sep='\n')
    plt.plot(x, y, 'rx' , label='Daten')
    plt.plot(t, f(t, *parameters), 'b-', label='Fit')
    plt.xlim(t[0], t[-1])
    plt.xlabel(r'$t$')
    plt.ylabel(r'$f(t)$')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(name)


y, x = np.genfromtxt('Gleichstrom', unpack=True)
plot(x, y, 'Gleichstrom')

y, x = np.genfromtxt('GleichstromR', unpack=True)
plot(x, y, 'GleichstromR')

y, x = np.genfromtxt('Aufgabed_Rechteckspannung.txt', unpack=True)
plot(x, y, 'Rechteck')

y, x = np.genfromtxt('Aufgabed_Sinusspannung.txt', unpack=True)
plot(x, y, 'Sinus')
