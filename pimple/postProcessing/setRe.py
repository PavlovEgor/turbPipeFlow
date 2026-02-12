
import re

def setU(path, U):
    with open(path + "0.orig/U", 'r') as file:
        content = file.read()

    # Ищем строку с value uniform ( ... );
    pattern = r'(value\s+uniform\s*\(\s*\d+\s+\d+\s+\d+\s*\);)'
    replacement = f'value           uniform (0 0 {U});'

    # Заменяем найденное значение
    new_content = re.sub(pattern, replacement, content)

    with open(path + "0.orig/U", 'w') as file:
        file.write(new_content)
        

def ReToU(Re, D=0.01, nu=1e-6):
    return nu * Re / D