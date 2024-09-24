from Mathlib import *
from math import atan2, acos, pi
from intercept import *
class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"
        
    def ray_intersect(self, orig, dir):
        return None
    
    
class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type= "Sphere"
        
    def ray_intersect(self, orig, dir):
        # Resta la posición del objeto con el origen del rayo
        L = subtract_vectors(self.position, orig)
        
        # Proyección del vector L en la dirección del rayo
        tca = dotProd(L, dir)
        
        # Magnitud de L
        L_magnitude = magnitude_vect(L)
        
        # Evitar raíces de números negativos
        L2_minus_tca2 = L_magnitude**2 - tca**2
        if L2_minus_tca2 < 0:
            return None  # Si es negativo, no hay intersección
        
        # Calcular d
        d = (L2_minus_tca2) ** 0.5
        
        # Comprobar si el rayo está fuera del radio de la esfera
        if d > self.radius:
            return None
        
        # Calcular thc
        thc = (self.radius**2 - d**2) ** 0.5
        
        # Calcular los puntos de intersección t0 y t1
        t0 = tca - thc
        t1 = tca + thc
        
        # Si t0 es negativo, usamos t1
        if t0 < 0:
            t0 = t1
        
        # Si t0 sigue siendo negativo, no hay intersección
        if t0 < 0:
            return None
        
        # Calcular el punto de intersección
        x = mult_scalar_vect(dir, t0)
        P = add_fully(orig, x)
        
        # Calcular la normal en el punto de intersección
        normal = subtract_fully(P, self.position)
        normal = normalize_vector(normal)
        
        # Calcular coordenadas de textura (u, v)
        u = (atan2(normal[2], normal[0])) / (2 * pi) + 0.5
        v = acos(-normal[1]) / pi
        
        # Devolver la información de la intersección
        return Intercept(
            point=P,
            normal=normal,
            distance=t0,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self
        )
