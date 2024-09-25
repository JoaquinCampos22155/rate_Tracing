from math import cos, sin, pi
import math
#operaciones de matrices
def normalize_vector(v):
    magnitude = math.sqrt(sum(vi**2 for vi in v))
    if magnitude == 0:
        return [0] * len(v)
    return [vi / magnitude for vi in v]
def custom_subtract(a, b):
    # Verificar si ambas listas tienen el mismo tamaño
    if len(a) != len(b):
        raise ValueError("Los arrays deben tener el mismo tamaño.")
    
    # Restar cada elemento correspondiente
    return [a[i] - b[i] for i in range(len(a))]
def custom_add(a, b):
    # Verificar si ambas listas tienen el mismo tamaño
    if len(a) != len(b):
        raise ValueError("Los arrays deben tener el mismo tamaño.")
    
    # Sumar cada elemento correspondiente
    return [a[i] + b[i] for i in range(len(a))]

def producto_punto_con_su_mismo(vector):
    return sum(x * x for x in vector)
def elevar_componentes_al_cuadrado(vector):
    return [x**2 for x in vector]
def magnitude_vect(v):
    return math.sqrt(sum([x**2 for x in v]))
def adjust_color(color, proportion):

    # Aseguramos que la proporción esté en el rango [0, 1]
    proportion = min(max(proportion, 0), 1)

    # Normalizamos y ajustamos el color
    adjusted_color = [min(max(int(c * proportion), 0), 255) for c in color]

    return adjusted_color

def add_fully(v1, v2):
    # Convertir los vectores a listas si no lo son
    v1 = list(v1) if not isinstance(v1, list) else v1
    v2 = list(v2) if not isinstance(v2, list) else v2
    
    # Verificar que los elementos dentro de los vectores sean numéricos
    if not all(isinstance(x, (int, float)) for x in v1):
        raise ValueError(f"Error: v1 contiene elementos no numéricos. v1: {v1}")
    
    if not all(isinstance(x, (int, float)) for x in v2):
        raise ValueError(f"Error: v2 contiene elementos no numéricos. v2: {v2}")
    
    # Si alguno de los vectores es vacío, retornar el otro
    if len(v1) == 0:
        return v2
    if len(v2) == 0:
        return v1
    
    # Extender el tamaño de los vectores para que tengan la misma longitud
    max_len = max(len(v1), len(v2))
    v1_extended = v1 + [0] * (max_len - len(v1))
    v2_extended = v2 + [0] * (max_len - len(v2))
    
    # Sumar elemento a elemento
    return [x + y for x, y in zip(v1_extended, v2_extended)]
def add_vectors(v1, v2):
    # Asegurarse de que v1 y v2 sean listas
    if not isinstance(v1, list) or not isinstance(v2, list):
        raise ValueError(f"Error: Ambos vectores deben ser listas. v1: {v1}, v2: {v2}")
    
    # Verificar si uno de los vectores es vacío
    if len(v1) == 0 or len(v2) == 0:
        raise ValueError(f"Error: uno de los vectores está vacío. v1: {v1}, v2: {v2}")
    
    # Suma de vectores
    max_len = max(len(v1), len(v2))
    
    # Extender los vectores para que tengan la misma longitud usando 0 como relleno
    v1_extended = v1 + [0] * (max_len - len(v1))
    v2_extended = v2 + [0] * (max_len - len(v2))
    
    # Sumar elemento a elemento
    return [x + y for x, y in zip(v1_extended, v2_extended)]
def invert_vector(vector):
    return [x * -1 for x in vector]

def add_scalar_to_vector(scalar, vector):
    #suma escalar por vector
    return [x + scalar for x in vector]
    
#multiplicacion escalar por vector.
def mult_scalar_vect(vector, scalar):
    return[x * scalar for x in vector]
def divide_vectors(v1, v2):
    return [x / y for x, y in zip(v1, v2)]

def subtract_vectors(v1, v2):
    # Resta de vectores
    return [x - y for x, y in zip(v1, v2)]
def subtract_fully(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a - b
    
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            raise ValueError("Las dimensiones no coinciden.")
        return [subtract_fully(x, y) for x, y in zip(a, b)]
    
    if isinstance(a, (int, float)) and isinstance(b, (list, tuple)):
        return [subtract_fully(a, x) for x in b]
    
    if isinstance(b, (int, float)) and isinstance(a, (list, tuple)):
        return [subtract_fully(x, b) for x in a]
    
    
    raise TypeError("Los tipos de datos no son compatibles para la resta.")

def dotProd(vec1, vec2):
    return sum(vi * vj for vi, vj in zip(vec1, vec2))
def crossProd(mat1, mat2):
    return [
        mat1[1] * mat2[2] - mat1[2] * mat2[1],  
        -(mat1[0] * mat2[2] - mat1[2] * mat2[0]), 
        mat1[0] * mat2[1] - mat1[1] * mat2[0]  
    ]

#mult elemento por elemento
def multExE(mat1, mat2):
    if not isinstance(mat2[0], list): 
        mat2 = [mat2 for _ in range(4)]

    result = [[mat1[i][j] * mat2[i][j] for j in range(4)] for i in range(4)]
    return result
#mult matriz vector
def matrix_vector_mult(matrix, vector):
    result = [0, 0, 0, 0]
    for i in range(4):
        result[i] = sum(matrix[i][j] * vector[j] for j in range(4))
    return result

#matriz 4x4 mult 
def matrixMult(matrix1, matrix2):
    result = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0], 
                 [0, 0, 0, 0]]

    for i in range(4):
        for j in range(4):
            result[i][j] = matrix1[i][0] * matrix2[0][j] + matrix1[i][1] * matrix2[1][j] + matrix1[i][2] * matrix2[2][j] + matrix1[i][3] * matrix2[3][j]
    return result

#matriz inversa
def inverseMatrix(matrix):
    
    n = 4
    mat = [row[:] for row in matrix]
    identity = [[float(i == j) for j in range(n)] for i in range(n)]

    #GJ
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(mat[k][i]) > abs(mat[max_row][i]):
                max_row = k

        mat[i], mat[max_row] = mat[max_row], mat[i]
        identity[i], identity[max_row] = identity[max_row], identity[i]

        pivot = mat[i][i]
        if pivot == 0:
            return None  

        for j in range(n):
            mat[i][j] /= pivot
            identity[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = mat[k][i]
                for j in range(n):
                    mat[k][j] -= factor * mat[i][j]
                    identity[k][j] -= factor * identity[i][j]
    return identity

#coordenadas baricentricas
def barycentricCoords(A, B, C, P):
	
	areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
				  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

	areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

	areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

	areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

	if areaABC == 0:
		return None

	
	u = areaPCB / areaABC
	v = areaACP / areaABC
	w = areaABP / areaABC


	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1:
		return (u, v, w)
	else:
		return None

#Render de clase 2 matrices de pos, tamaño y rotacion 
def TranslationMatrix(x, y, z):
    matrixT = [[1, 0, 0, x],
               [0, 1, 0, y],
               [0, 0, 1, z],
               [0, 0, 0, 1]]
    return matrixT

def toArray(vect):
    array = [] 
    for i in range(len(vect)):
        array.append(vect[i])
    return array

def ScaleMatrix(x, y, z):
    matrixS = [[x, 0, 0, 0],
               [0, y, 0, 0],
               [0, 0, z, 0],
               [0, 0, 0, 1]]
    return matrixS
def toList(array):
    if isinstance(array, (list, tuple)):  
        return [toList(item) for item in array]
    else: 
        return array

def RotationMatrix(pitch, yaw, roll):
    pitch *= pi / 180
    yaw *= pi / 180
    roll *= pi / 180
    
    pitchMat = [[1, 0, 0, 0],
                [0, cos(pitch), -sin(pitch), 0],
                [0, sin(pitch), cos(pitch), 0],
                [0, 0, 0, 1]]
    
    yawMat = [[cos(yaw), 0, sin(yaw), 0],
              [0, 1, 0, 0],
              [-sin(yaw), 0, cos(yaw), 0],
              [0, 0, 0, 1]]
    
    rollMat = [[cos(roll), -sin(roll), 0, 0],
               [sin(roll), cos(roll), 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]]
    
    resultM = [[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]
    
    intermediateM = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
    
    for i in range(4):
        for j in range(4):
            for k in range(4):
                intermediateM[i][j] += pitchMat[i][k] * yawMat[k][j]
    
    for i in range(4):
        for j in range(4):
            for k in range(4):
                resultM[i][j] += intermediateM[i][k] * rollMat[k][j]
    
    return resultM
def vector_add(v1, v2):
    return [v1[i] + v2[i] for i in range(len(v1))]

def vector_subtract(v1, v2):
    return [v1[i] - v2[i] for i in range(len(v1))]

def reflectVector(normal, direction):
    #R = 2*(N .L) *N - L
    normal_vector = normalize_vector(normal)
    normal_dir = normalize_vector(direction)
    
    reflect = dotProd(normal_vector, normal_dir)
    reflect = reflect * 2
    reflect = mult_scalar_vect(normal,reflect)
    reflect = subtract_vectors(reflect, direction)
    reflect = normalize_vector(reflect)
    return reflect

def cofactor(matriz, row, col):
    submatriz = [[matriz[i][j] for j in range(len(matriz)) if j != col] for i in range(len(matriz)) if i != row]
    return ((-1) ** (row + col)) * determinante(submatriz)

def determinante(matriz):
    if len(matriz) == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
    
    det = 0
    for col in range(len(matriz)):
        det += matriz[0][col] * cofactor(matriz, 0, col)
    return det
def linnorm(vector):
    # Calcula la suma de los cuadrados de los elementos
    suma_cuadrados = sum([x**2 for x in vector])
    # Devuelve la raíz cuadrada de la suma de los cuadrados
    return math.sqrt(suma_cuadrados)

def magnitudVector(v):
    return math.sqrt(sum(vi**2 for vi in v))

def normalizarVector(v):
    mag = magnitudVector(v)
    if mag == 0:
        return [0] * len(v)
    return [vi / mag for vi in v]

def productoPunto(v1, v2):
    return sum(vi * vj for vi, vj in zip(v1, v2))

def productoCruz(v1, v2):
    if len(v1) == 3 and len(v2) == 3:
        return [v1[1] * v2[2] - v1[2] * v2[1],
                v1[2] * v2[0] - v1[0] * v2[2],
                v1[0] * v2[1] - v1[1] * v2[0]]
    else:
        raise ValueError("El producto cruz solo está definido para vectores de 3 dimensiones")
    
def multiplicarPorEscalar(escalar, vector):
    return [escalar * componente for componente in vector]

