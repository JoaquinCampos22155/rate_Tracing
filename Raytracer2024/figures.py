from Mathlib import *
from math import atan2, acos, pi
from intercept import *
import numpy as np
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
            return None  
        
        d = (L2_minus_tca2) ** 0.5
        
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
        
        P = [orig[i] + dir[i] * t0 for i in range(3)]
        normal = [P[i] - self.position[i] for i in range(3)]
        
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

class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        R = magnitude_vect(normal)
        for i in range(len(normal)):
            normal[i] /= R
        self.normal = normal
        self.type == "Plane"
        
    def ray_intersect(self, orig, dir):
        #t(distance) = ((planePos - rayOrigin) dotProd(normal))/ rayDir dotProd(normal)
        
        denom = dotProd(dir, self.normal)
        if math.isclose(0, denom):
            return None
        x = subtract_vectors(self.position, orig)
        num = dotProd(x, self.normal)
        t = num/denom
        
        if t < 0:
            return None
        #P = orig +  dir * t0
        
        #np.array(dir)
        x = toArray(dir)
        y = mult_scalar_vect(x, t)
        P = [orig[i] + y[i] for i in range(3)]

        return Intercept(point = P,
                        normal=self.normal,
                        distance = t,
                        texCoords= None,
                        rayDirection=dir,
                        obj = self)
        
class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius
        self.type = "Disk"
        
    def ray_intersect(self, orig, dir):
        planeIntercept = super().ray_intersect(orig, dir)
        
        if planeIntercept is None:
            return None
        contact = subtract_vectors(planeIntercept.point, self.position)
        contact = magnitude_vect(contact)
        
        if contact > self.radius:
            return None
        
        return planeIntercept
    
class AABB(Shape):
    # Axis Aligned Bounding Box
    #OBB : Oriented Bounding Box
    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"
        
        self.planes = []
        
        rightPlane = Plane([position[0] + sizes[0]/2, position[1], position[2]], [1,0,0], material)
        leftPlane = Plane( [position[0] - sizes[0]/2, position[1], position[2]], [-1,0,0], material)
        
        upPlane = Plane( [position[0] , position[1]+ sizes[1] /2, position[2]], [0,1,0], material)
        downPlane = Plane( [position[0] , position[1]- sizes[1] /2, position[2]], [0,-1,0], material)


        frontPlane = Plane( [position[0] , position[1], position[2] + sizes[2]/2], [0,0,1], material)
        backPlane = Plane( [position[0] , position[1], position[2] - sizes[2]/2], [0,0,-1], material)
        
        self.planes.append(rightPlane)
        self.planes.append(leftPlane)
        self.planes.append(upPlane)
        self.planes.append(downPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)
        
        #Bounds
        self.boundMin = [0,0,0]
        self.boundMax = [0,0,0]
        
        epsilon = 0.001
        
        for i in range(3):
            self.boundMin[i] = position[i] - (epsilon + sizes[i]/2)
            self.boundMax[i] = position[i] + (epsilon + sizes[i]/2)
            
    def ray_intersect(self, orig, dir):
        intercept = None
        t = float("inf")
        for plane in self.planes:
            planeIntercept = plane.ray_intersect(orig, dir)
            
            if planeIntercept is not None:
                planePoint = planeIntercept.point
                
                if self.boundMin[0] <= planePoint[0] <= self.boundMax[0]:
                    if self.boundMin[1] <= planePoint[1] <= self.boundMax[1]:
                        if self.boundMin[2] <= planePoint[2] <= self.boundMax[2]:
                            
                            if planeIntercept.distance < t:
                                t = planeIntercept.distance
                                intercept = planeIntercept
                                
        if intercept == None:
            return None
        
        u,v = 0,0
        
        if abs(intercept.normal[0])> 0:
            #mapera las uvs apra el eje x, usando las coords de y y z
            u = (intercept.point[1] - self.boundMin[1])/self.sizes[1]
            v = (intercept.point[2] - self.boundMin[2])/self.sizes[2]
        elif abs(intercept.normal[1])> 0:
            #mapera las uvs apra el eje x, usando las coords de y y z
            u = (intercept.point[0] - self.boundMin[0])/self.sizes[0]
            v = (intercept.point[2] - self.boundMin[2])/self.sizes[2]  
        elif abs(intercept.normal[2])> 0:
            #mapera las uvs apra el eje x, usando las coords de y y z
            u = (intercept.point[0] - self.boundMin[0])/self.sizes[0]
            v = (intercept.point[1] - self.boundMin[1])/self.sizes[1]                      
        
        u = min(0.999, max(0, u))
        v = min(0.999, max(0, v))
        return Intercept(point= intercept.point,
                         normal= intercept.normal,
                         distance= t,
                         texCoords = [u,v],
                         rayDirection= dir,
                         obj= self)
class Triangle(Shape):        
    def __init__(self, v0, v1, v2, material):
        super().__init__(v0, material)
        self.v0 = v0 
        self.v1 = v1 
        self.v2 = v2 
        self.type = "Triangle"
        
        # Calcular el vector normal del triángulo
        self.normal = cross_product(subtract_vectors(v1, v0), subtract_vectors(v2, v0))
        self.normal = normalize_vector(self.normal)
        
    def ray_intersect(self, orig, dir):
        # Método de intersección de rayo con triángulo
        # Utiliza el algoritmo de Möller–Trumbore para una intersección eficiente

        epsilon = 1e-6
        edge1 = subtract_vectors(self.v1, self.v0)
        edge2 = subtract_vectors(self.v2, self.v0)
        h = cross_product(dir, edge2)
        a = dotProd(edge1, h)
        
        if -epsilon < a < epsilon:
            return None  # El rayo es paralelo al triángulo
        
        f = 1.0 / a
        s = subtract_vectors(orig, self.v0)
        u = f * dotProd(s, h)
        
        if u < 0.0 or u > 1.0:
            return None  # El punto de intersección está fuera del triángulo
        
        q = cross_product(s, edge1)
        v = f * dotProd(dir, q)
        
        if v < 0.0 or u + v > 1.0:
            return None  # El punto de intersección está fuera del triángulo
        
        t = f * dotProd(edge2, q)
        
        if t < epsilon:
            return None  # No hay intersección
        
        # Calcular el punto de intersección
        P = orig + mult_scalar_vect(dir, t)
        # Devolver la información de la intersección
        return Intercept(
            point=P,
            normal=self.normal,
            distance=t,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self
        )
class Cylinder(Shape):
    def __init__(self, position, radius, height, normal, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.normal = normalize_vector(normal)
        self.type = "Cylinder"
        
        # Vamos a construir una base ortonormal usando el vector normal
        self.transformation_matrix = self.build_transformation_matrix(self.normal)
        self.inverse_transformation_matrix = np.linalg.inv(self.transformation_matrix)
    
    def build_transformation_matrix(self, normal):
        # Crear una base ortonormal: usando el normal como eje z del nuevo sistema
        # Usamos un vector arbitrario que no sea paralelo para calcular la base
        z = normalize_vector(normal)
        x = [1, 0, 0] if abs(z[0]) < 0.9 else [0, 1, 0]  # Vector arbitrario no colineal
        
        # Calculamos el vector ortogonal usando el producto cruzado
        x = normalize_vector(np.cross(z, x))
        y = np.cross(z, x)
        
        # Creamos la matriz de transformación de coordenadas
        return np.array([x, y, z]).T
    
    def ray_intersect(self, orig, dir):
        # Transformar las coordenadas del rayo al sistema de referencia del cilindro
        orig_local = np.dot(self.inverse_transformation_matrix, subtract_vectors(orig, self.position))
        dir_local = np.dot(self.inverse_transformation_matrix, dir)
        
        # Intersección en el espacio local del cilindro (orientado a lo largo del eje Y)
        dx, dz = dir_local[0], dir_local[2]
        ox, oz = orig_local[0], orig_local[2]
        
        a = dx * dx + dz * dz
        b = 2 * (ox * dx + oz * dz)
        c = ox * ox + oz * oz - self.radius * self.radius
        
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return None  # No hay intersección
        
        sqrt_discriminant = discriminant ** 0.5
        t0 = (-b - sqrt_discriminant) / (2 * a)
        t1 = (-b + sqrt_discriminant) / (2 * a)
        
        if t0 > t1:
            t0, t1 = t1, t0
        
        # Calcular la intersección más cercana dentro del rango del cilindro (altura)
        y0 = orig_local[1] + t0 * dir_local[1]
        y1 = orig_local[1] + t1 * dir_local[1]
        
        if y0 < 0 or y0 > self.height:
            t0 = None
        if y1 < 0 or y1 > self.height:
            t1 = None
            
        if t0 is None and t1 is None:
            return None  # No intersección dentro de la altura del cilindro
        
        t = t0 if t0 is not None else t1
        
        if t < 0:
            return None  # La intersección está detrás de la cámara
        
        # Punto de intersección en el espacio local
        P_local = [orig_local[i] + dir_local[i] * t for i in range(3)]
        
        # Normal del cilindro en el punto de intersección en el espacio local
        normal_local = [P_local[0], 0, P_local[2]]
        normal_local = normalize_vector(normal_local)
        
        # Convertimos el punto de intersección y la normal de vuelta al espacio global
        P_world = np.dot(self.transformation_matrix, P_local) + self.position
        normal_world = np.dot(self.transformation_matrix, normal_local)
        normal_world = normalize_vector(normal_world)
        
        # Coordenadas de textura
        u = (atan2(P_local[2], P_local[0]) / (2 * pi)) + 0.5
        v = P_local[1] / self.height
        
        u = max(0, min(0.999, u))
        v = max(0, min(0.999, v))
        
        return Intercept(
            point=P_world,
            normal=normal_world,
            distance=t,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self
        )