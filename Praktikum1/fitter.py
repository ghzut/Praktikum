import numpy as np
import matplotlib.pyplot as plt

x, y = np.genfromtxt('data.txt', unpack=True)
x = x/19
y = y/(np.sqrt(2)*2)
# x2 = np.linspace(20/380, 30000/380, 10000)
x3 = np.array([2, 3, 4, 5, 7, 10])
x2 = np.append(x, x3/19)
print(x2)
print(x3)
y2 = np.sqrt((1/9)*(((x2**2)-1)**2)/((1-(x2**2))**2+(9*(x2**2))))
print(y2)
plt.plot(x2, y2, 'r', label=r'$g(x)$')
plt.plot(x, y, 'b.', label='Messwerte')
plt.xscale('log')
plt.ylabel(r'$U_b/U_s$')
plt.xlabel(r'$v/v_0$')

plt.legend(loc='best')
plt.show()
