import openfoamparser_mai as Ofpp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
import re
import subprocess
import time


def setControlDict(path, U, L=0.55):
    with open(path + "system/controlDict", 'r') as file:
        content = file.read()

    T = 0.2 * L / U
    # Ищем строку с value uniform ( ... );
    pattern = r'(endTime\s+)[\d\.]+;'
    replacement = f'endTime         {T};'

    # Заменяем найденное значение
    new_content = re.sub(pattern, replacement, content)

    with open(path + "system/controlDict", 'w') as file:
        file.write(new_content)


path = "/home/user/OpenFOAM/user-v2412/run/turbPipeFlow/axisSymm/"

setControlDict(path, 1)

# subprocess.run([path + "Allrun"], check=True)

# subprocess.run([path + "Allclean"])
