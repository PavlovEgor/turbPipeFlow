import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

def BlasiusLow(Re):
    return 0.3164 / (Re ** 0.25)


def PrandlLow(Re):

    C = 0.8 - 2 * np.log10(Re)
    def PrFunc(x):
        return C + (x ** (-0.5)) - np.log10(x) 
    
    def PrFuncPrime(x):
        return -0.5 * (x ** (-1.5)) - np.log(10) / x
    
    root = newton(PrFunc, BlasiusLow(Re), PrFuncPrime)

    return root

print(PrandlLow(1e5))

n = 100
R = np.logspace(3.8, 6.4, n)
BL = BlasiusLow(R)
PL = PrandlLow(R)

# plt.plot(R, BL, label = "закон Блазиуса")

# result_filename_ke = "planeSymmReLambda_49280.txt"
result_filename_ke_22770 = "planeSymmReLambda_22770.txt"
result_filename_ke_49280 = "planeSymmReLambda_49280.txt"

R_CFD_ke_22770, Lambda_CFD_ke_22770, _, _, yPlusAve_22770= np.loadtxt(result_filename_ke_22770, comments='#').T
R_CFD_ke_49280, Lambda_CFD_ke_49280, _, _, yPlusAve_49280= np.loadtxt(result_filename_ke_49280, comments='#').T

fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

# ax1.plot(R, BL, label = "закон Блазиуса")
ax1.plot(R, PL, label = "закон Прандтля")
ax1.plot(R_CFD_ke_22770, Lambda_CFD_ke_22770, 'o', label="PlaneSymm KEpsilon_22770")
ax1.plot(R_CFD_ke_49280, Lambda_CFD_ke_49280, 'o', label="PlaneSymm KEpsilon_49280")

ax1.set_ylabel(r'$\lambda$', fontsize=16, color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax1.set_xlabel('$Re$', fontsize=16)
ax1.set_xscale('log')  
ax1.set_yscale('log')  
ax2.set_yscale('log')

ax2.plot(R_CFD_ke_22770, yPlusAve_22770, 'x', label="y+ PlaneSymm KEpsilon_22770")
ax2.plot(R_CFD_ke_49280, yPlusAve_49280, 'x', label="y+ PlaneSymm KEpsilon_49280")

ax2.set_ylabel('Average y+', color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:green')

# Отображение
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.tight_layout()

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper center')

plt.show()