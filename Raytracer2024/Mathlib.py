from math import cos, sin, pi
import math
#operaciones de matrices
#Normalizar vector
def normalize_vector(v):
    magnitude = math.sqrt(sum(vi**2 for vi in v))
    if magnitude == 0:
        return [0] * len(v)
    return [vi / magnitude for vi in v]
#magnitud vect
def magnitude_vect(v):
    return math.sqrt(sum([x**2 for x in v]))

def magnitudVector(v):
    return math.sqrt(sum(vi**2 for vi in v))

#multiplicacion escalar por vector.
def mult_scalar_vect(vector, scalar):
    return[x * scalar for x in vector]


def subtract_vectors(v1, v2):
    # Resta de vectores
    return [x - y for x, y in zip(v1, v2)]

def dotProd(vec1, vec2):
    return sum(vi * vj for vi, vj in zip(vec1, vec2))



#matriz inversa
def inverseMatrix(matrix):
    
    mat = [row[:] for row in matrix]
    identity = [[float(i == j) for j in range(4)] for i in range(4)]

    #GJ
    for i in range(4):
        max_row = i
        for k in range(i + 1, 4):
            if abs(mat[k][i]) > abs(mat[max_row][i]):
                max_row = k

        mat[i], mat[max_row] = mat[max_row], mat[i]
        identity[i], identity[max_row] = identity[max_row], identity[i]

        pivot = mat[i][i]
        if pivot == 0:
            return None  

        for j in range(4):
            mat[i][j] /= pivot
            identity[i][j] /= pivot

        for k in range(4):
            if k != i:
                factor = mat[k][i]
                for j in range(4):
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

def reflectVector(normal, direction):
    #R = 2*(N .L) *N - L
    normal_vector = normalize_vector(normal)
    normal_dir = normalize_vector(direction)
    
    reflect = dotProd(normal_vector, normal_dir)
    reflect = reflect * 2
    reflect = mult_scalar_vect(normal_dir,reflect)
    reflect = subtract_vectors(reflect, direction)
    reflect = normalize_vector(reflect)
    return reflect


def normalizarVector(v):
    mag = magnitudVector(v)
    if mag == 0:
        return [0] * len(v)
    return [vi / mag for vi in v]
