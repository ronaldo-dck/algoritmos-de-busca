import numpy as np

def codificar(matriz):
    codigo_x = 0
    codigo_o = 0

    for i in range(6):
        for j in range(7):
            index = i * 7 + j
            if matriz[i][j] == 'X':
                codigo_x |= 1 << index
            elif matriz[i][j] == 'O':
                codigo_o |= 1 << index

    return (codigo_x, codigo_o)


def decodificar(codigo_x, codigo_o):
    matriz = np.full((6, 7), ' ')

    for i in range(6):
        for j in range(7):
            index = i * 7 + j
            if (codigo_x & (1 << index)) != 0:
                matriz[i][j] = 'X'
            elif (codigo_o & (1 << index)) != 0:
                matriz[i][j] = 'O'

    return matriz


# Exemplo de uso:
A = np.array([
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'X', ' ', ' ', ' ', ' '],
    [' ', ' ', 'O', ' ', ' ', ' ', ' '],
    [' ', ' ', 'O', ' ', ' ', ' ', ' '],
    [' ', ' ', 'O', 'X', ' ', ' ', ' '],
    ['O', 'O', 'X', 'X', 'X', 'O', 'X'],
])

cod = codificar(A)
B = decodificar(cod[0], cod[1])


print("Matriz original:")
print(A)
print(cod)
print("\nMatriz decodificada:")
print(B)
