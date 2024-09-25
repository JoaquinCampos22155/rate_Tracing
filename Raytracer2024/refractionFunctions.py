from math import acos, asin, pi
from Mathlib import *

def refractVector(normal, incident, n1, n2):
# Convertir los parámetros a listas
    normal = list(normal)
    incident = list(incident)
    
    # Ley de Snell
    c1 = dotProd(normal, incident)
    
    if c1 < 0:
        c1 = -c1
    else:
        normal = mult_scalar_vect(normal,-1 )
        n1, n2 = n2, n1

    n = n1 / n2
    
    # Fórmula de refracción
    T1 = mult_scalar_vect([incident[i] + c1 * normal[i] for i in range(3)],n)
    T2 = mult_scalar_vect(normal, -1)
    T = [T1[i] + T2[i] * (1 - n**2 * (1 - c1**2))**0.5 for i in range(3)]
    
    # Normalizar el vector resultante
    return normalize_vector(T)
    
def totalInternalReflection(normal, incident, n1, n2):
	c1 = dotProd(normal, incident)
	if c1 < 0:
		c1 = -c1
	else:
		n1, n2 = n2, n1
		
	if n1 < n2:
		return False
	
	theta1 = math.acos(c1)
	thetaC = math.asin(n2/n1)
	
	return theta1 >= thetaC


def fresnel(normal, incident, n1, n2):
	c1 = dotProd(normal, incident)
	if c1 < 0:
		c1 = -c1
	else:
		n1, n2 = n2, n1

	s2 = (n1 * (1 - c1**2)**0.5) / n2
	c2 = (1 - s2 ** 2) ** 0.5
	
	F1 = (((n2 * c1) - (n1 * c2)) / ((n2 * c1) + (n1 * c2))) ** 2
	F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 * c1))) ** 2

	Kr = (F1 + F2) / 2
	Kt = 1 - Kr
	return Kr, Kt