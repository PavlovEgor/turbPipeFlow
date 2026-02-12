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

n = 100
R = np.logspace(4.1, 6.4, n)
BL = BlasiusLow(R)
PL = PrandlLow(R)

# plt.plot(R, BL, label = "закон Блазиуса")
plt.plot(R, PL, label = "закон Прандтля")


result_filename_ke_67473 = "fullTaskReLambdaKEpsilon_67473.txt"
result_filename_ke_162000 = "fullTaskReLambdaKEpsilon_162000.txt"

result_filename_ko = "fullTaskReLambdaKOmega.txt"

R_CFD_ke_67473, Lambda_CFD_ke_67473 = np.loadtxt(result_filename_ke_67473, comments='#').T
R_CFD_ke_162000, Lambda_CFD_ke_162000 = np.loadtxt(result_filename_ke_162000, comments='#').T

# R_CFD_ko, Lambda_CFD_ko = np.loadtxt(result_filename_ko, comments='#').T

plt.plot(R_CFD_ke_67473, Lambda_CFD_ke_67473, 'o', label="FullTask KEpsilon 67473")
plt.plot(R_CFD_ke_162000, Lambda_CFD_ke_162000, 'o', label="FullTask KEpsilon 162000")

# plt.plot(R_CFD_ko, Lambda_CFD_ko, 'o', label="FullTask KOmega")

plt.xlabel('$Re$', fontsize=16)
plt.ylabel(r'$\lambda$', fontsize=16)
plt.xscale('log')  # Логарифмический масштаб по оси X
plt.yscale('log')  # Логарифмический масштаб по оси Y
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.legend()

plt.show()
