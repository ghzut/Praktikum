import numpy as np
import matplotlib.pyplot as plt
import uncertainties as unc

x, y = np.genfromtxt('data.txt', unpack=True)
x = x/19
plt.plot(x, y, 'b.')
plt.xscale('log')

plt.show()
