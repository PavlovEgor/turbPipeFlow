import numpy as np
import matplotlib.pyplot as plt
import re
import subprocess
import pandas as pd
from scipy.optimize import newton


def Lambda(dP, Re, D=0.01, L=0.5, nu=1e-6):
    return (dP / (Re ** 2)) * ((2 * (D ** 3)) / (L * (nu ** 2)))


def setU(path, U):
    with open(path + "0.orig/U", 'r') as file:
        content = file.read()

    # Ищем строку с value uniform ( ... );
    pattern = r'(value\s+uniform\s*\(\s*[\d\.]+\s+[\d\.]+\s+[\d\.]+\s*\);)'
    replacement = f'value           uniform (0 0 {U});'

    # Заменяем найденное значение
    new_content = re.sub(pattern, replacement, content)

    with open(path + "0.orig/U", 'w') as file:
        file.write(new_content)


def setControlDict(path, U, L=0.55):
    with open(path + "system/controlDict", 'r') as file:
        content = file.read()

    T = 0.2 * L / U
    # Ищем строку с value uniform ( ... );
    pattern = r'(endTime\s+)[\d\.]+;'
    replacement = f'endTime         {T};'

    pattern2 = r'(writeInterval\s+)[\d\.]+;'
    replacement2 = f'writeInterval         {T/10};'

    # Заменяем найденное значение
    new_content = re.sub(pattern, replacement, content)
    new_content = re.sub(pattern2, replacement2, new_content)

    with open(path + "system/controlDict", 'w') as file:
        file.write(new_content)

def setTurbModel(path, modelName):
    with open(path + "constant/turbulenceProperties", 'r') as file:
        content = file.read()

    # Ищем строку с value uniform ( ... );
    pattern = r'(RASModel\s+)\w+;'
    replacement = f'    RASModel    {modelName};'

    # Заменяем найденное значение
    new_content = re.sub(pattern, replacement, content)

    with open(path + "constant/turbulenceProperties", 'w') as file:
        file.write(new_content)


def ReToU(Re, D=0.01, nu=1e-6):
    return nu * Re / D

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


path = "../"
result_filename = "planeSymmReLambda.txt"

turbulenceModels = [
    # "LRR", #
    "LamBremhorstKE",
    "LaunderSharmaKE",
    "LienCubicKE",
    "LienLeschziner",
    "RNGkEpsilon",
    # "SSG", #
    "ShihQuadraticKE",
    "SpalartAllmaras",
    "kEpsilon",
    # "kEpsilonLopesdaCosta", #
    # "kEpsilonPhitF", #
    # "kOmega2006", #
    "kOmegaSST",
    # "kOmegaSSTLM",
    # "kOmegaSSTSAS", #
    "kkLOmega",
    # "qZeta",
    # "realizableKE",
    # "v2f"
]

result = pd.DataFrame({"P": [0] * len(turbulenceModels),
                       "minYPlus": [0] * len(turbulenceModels),
                       "maxYPlus": [0] * len(turbulenceModels),
                       "aveYPlus": [0] * len(turbulenceModels),
                       "lambda": [0] * len(turbulenceModels),
                       "turbModelName": turbulenceModels})

Re = 1e5
U = ReToU(Re)
setU(path, U)
print("Re= ", Re, "U= ", U)

for i, modelName in enumerate(turbulenceModels):

    setTurbModel(path, modelName)

    subprocess.run([path + "Allclean"])
    subprocess.run([path + "Allrun"], check=True)
    
    p_data = np.loadtxt(path + "postProcessing/probes/0/p", comments='#')
    yPlus_data = np.loadtxt(path + "postProcessing/yPlus/0/yPlus.dat",     
                            comments='#',  # Пропускаем строки, начинающиеся с #
                            usecols=(0, 2, 3, 4)
                            )
    print("P=", p_data[-1][1], 
          "min y+= ", yPlus_data[-1][1], 
          "max y+= ", yPlus_data[-1][2], 
          "ave y+= ", yPlus_data[-1][3], 
          "lambda= ", Lambda(p_data[-1][1], Re))

    result.loc[i, "P"]          = p_data[-1][1]
    result.loc[i, "minYPlus"]   = yPlus_data[-1][1]
    result.loc[i, "maxYPlus"]   = yPlus_data[-1][2]
    result.loc[i, "aveYPlus"]   = yPlus_data[-1][3]
    result.loc[i, "lambda"]     = Lambda(p_data[-1][1], Re)


result.to_csv(path + "postProcessingPy/" + result_filename)

print(result)
print("Re= ", Re, "Prandl lambda= ",  PrandlLow(Re))