import numpy as np
from math import acos, asin, pi
from Mathlib import *

def refractVector(normal, incident, n1, n2):

    normal = toArray(normal)
    incident = toArray(incident)
    
    # Ley de Snell
    c1 = dotProd(normal, incident)
    
    if c1 < 0:
        c1 = -c1
    else:
        normal = invert_vector(normal)
        n1, n2 = n2, n1

    n = n1 / n2
    a = mult_scalar_vect(normal, c1)
    b = mult_scalar_vect(incident +a, n)
    c = mult_scalar_vect(normal, (1 - n**2 * (1 - c1**2 )) ** 0.5)
    T = subtract_vectors(b ,c)
    
    return T / np.linalg.norm(T)

def totalInternalReflection(normal, incident, n1, n2):
	c1 = dotProd(normal, incident)
	if c1 < 0:
		c1 = -c1
	else:
		n1, n2 = n2, n1
		
	if n1 < n2:
		return False
	
	theta1 = acos(c1)
	thetaC = asin(n2/n1)
	
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