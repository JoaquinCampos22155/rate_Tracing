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
        
        # Construimos la matriz de transformación con el vector normal
        self.transformation_matrix = self.build_transformation_matrix(self.normal)
        self.inverse_transformation_matrix = self.transpose_matrix(self.transformation_matrix)  # Inversión de matriz ortogonal
    
    def build_transformation_matrix(self, normal):
        # Crear una base ortonormal usando el normal como eje Z
        z = normalize_vector(normal)
        x = [1, 0, 0] if abs(z[0]) < 0.9 else [0, 1, 0]  # Vector arbitrario no colineal

        # Calcular el vector ortogonal usando el producto cruzado
        x = normalize_vector(cross_product(z, x))
        y = cross_product(z, x)

        # Crear la matriz de transformación (3x3)
        return [[x[0], y[0], z[0]],
                [x[1], y[1], z[1]],
                [x[2], y[2], z[2]]]
    
    def transpose_matrix(self, matrix):
        # Transponer la matriz (inversión de matriz ortogonal)
        return [[matrix[j][i] for j in range(3)] for i in range(3)]
    
    def ray_intersect(self, orig, dir):
        # Transformar las coordenadas del rayo al sistema de referencia del cilindro
        orig_local = dotProdmtvc(self.inverse_transformation_matrix, subtract_vectors(orig, self.position))
        dir_local = dotProdmtvc(self.inverse_transformation_matrix, dir)
        
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
            return None  # No hay intersección dentro de la altura del cilindro
        
        t = t0 if t0 is not None else t1
        
        if t < 0:
            return None  # La intersección está detrás de la cámara
        
        # Punto de intersección en el espacio local
        P_local = [orig_local[i] + dir_local[i] * t for i in range(3)]
        
        # Normal del cilindro en el punto de intersección en el espacio local
        normal_local = [P_local[0], 0, P_local[2]]
        normal_local = normalize_vector(normal_local)
        
        # Convertir el punto de intersección y la normal de vuelta al espacio global
        P_world = add_vectors(dotProdmtvc(self.transformation_matrix, P_local), self.position)
        normal_world = dotProdmtvc(self.transformation_matrix, normal_local)
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
class Ellipsoid(Shape):
    def __init__(self, position, radii, material):
        super().__init__(position, material)
        self.radii = radii  # Radii should be a list or tuple [rx, ry, rz]
        self.type = "Ellipsoid"
    
    def ray_intersect(self, orig, dir):
        # Rescalar el origen y la dirección del rayo según los radios del elipsoide
        scaled_orig = [orig[i] / self.radii[i] for i in range(3)]
        scaled_dir = [dir[i] / self.radii[i] for i in range(3)]
        
        # Utilizamos la misma fórmula que para la esfera con el origen y la dirección escalados
        L = subtract_vectors(self.position, scaled_orig)
        tca = dotProd(L, scaled_dir)
        L_magnitude = magnitude_vect(L)
        d2 = L_magnitude ** 2 - tca ** 2
        
        if d2 > 1:  # El punto más cercano al rayo está fuera del elipsoide
            return None
        
        thc = (1 - d2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        
        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        # Calcular el punto de intersección
        P = [scaled_orig[i] + scaled_dir[i] * t0 for i in range(3)]
        # Escalamos de vuelta a las coordenadas originales
        P_world = [P[i] * self.radii[i] for i in range(3)]
        normal = normalize_vector([P_world[i] - self.position[i] for i in range(3)])
        
        u = (atan2(normal[2], normal[0])) / (2 * pi) + 0.5
        v = acos(-normal[1]) / pi
        
        return Intercept(
            point=P_world,
            normal=normal,
            distance=t0,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self
        )
###
class HexagonalPrism(Shape):
    def __init__(self, position, radius, height, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.type = "HexagonalPrism"
        
        # Crear los seis planos que forman los lados del prisma
        self.planes = []
        for i in range(6):
            angle = (pi / 3) * i  # El ángulo correcto entre las caras es pi/3
            normal = [cos(angle), 0, sin(angle)]  # Normales de los planos laterales
            plane_position = [position[0] + cos(angle) * radius, position[1], position[2] + sin(angle) * radius]
            self.planes.append(Plane(plane_position, normal, material))
        
        # Crear los planos superior e inferior
        self.top_plane = Plane([position[0], position[1] + height / 2, position[2]], [0, 1, 0], material)
        self.bottom_plane = Plane([position[0], position[1] - height / 2, position[2]], [0, -1, 0], material)
    
    def ray_intersect(self, orig, dir):
        closest_intercept = None
        min_distance = float("inf")
        
        # Verificar intersección con los planos laterales
        for plane in self.planes:
            intercept = plane.ray_intersect(orig, dir)
            if intercept and intercept.distance < min_distance:
                # Comprobar si el punto está dentro de la altura del prisma
                if abs(intercept.point[1] - self.position[1]) <= self.height / 2:
                    closest_intercept = intercept
                    min_distance = intercept.distance
        
        # Verificar intersección con los planos superior e inferior
        for plane in [self.top_plane, self.bottom_plane]:
            intercept = plane.ray_intersect(orig, dir)
            if intercept and intercept.distance < min_distance:
                # Comprobar si el punto está dentro del hexágono
                point_2d = [intercept.point[0] - self.position[0], intercept.point[2] - self.position[2]]
                if magnitude_vect(point_2d) <= self.radius:
                    closest_intercept = intercept
                    min_distance = intercept.distance
        
        return closest_intercept

class Star(Shape):
    def __init__(self, position, size, material):
        super().__init__(position, material)
        self.size = size
        self.type = "Star"
        
    def ray_intersect(self, orig, dir):
        # La intersección es en 2D, por lo que reducimos a 2D
        num_points = 5  # Número de picos de la estrella
        angle_step = 2 * math.pi / num_points
        star_points = []
        
        # Generar los puntos de la estrella (alternando puntos interiores y exteriores)
        for i in range(num_points * 2):
            angle = i * angle_step / 2
            r = self.size if i % 2 == 0 else self.size * 0.5
            x = self.position[0] + r * math.cos(angle)
            y = self.position[1] + r * math.sin(angle)
            star_points.append([x, y])
        
        # Verificar si el rayo cruza algún borde del polígono formado por la estrella
        min_distance = float("inf")
        closest_point = None
        for i in range(len(star_points)):
            p0 = star_points[i]
            p1 = star_points[(i + 1) % len(star_points)]
            
            # Ver si el rayo cruza este borde (en 2D)
            edge = subtract_vectors(p1, p0)  # Operamos en 2D
            to_origin = subtract_vectors(orig[:2], p0)  # Consideramos solo las coordenadas X e Y
            dir_2d = dir[:2]  # Solo tomamos el componente 2D del rayo
            
            # Cálculo del determinante para evitar división por cero
            det = dir_2d[0] * edge[1] - dir_2d[1] * edge[0]
            if math.isclose(det, 0):
                continue  # El rayo es paralelo al borde
            
            # Cálculos de t y u usando determinantes (intersección de segmentos)
            t = (to_origin[0] * edge[1] - to_origin[1] * edge[0]) / det
            u = (to_origin[0] * dir_2d[1] - to_origin[1] * dir_2d[0]) / det
            
            if 0 <= u <= 1 and t >= 0:  # Intersección válida
                intersection_point = [orig[0] + dir[0] * t, orig[1] + dir[1] * t]
                distance = magnitude_vect(subtract_vectors(intersection_point, orig[:2]))
                if distance < min_distance:
                    min_distance = distance
                    closest_point = intersection_point
        
        if closest_point is None:
            return None
        
        # Normal de la estrella en el punto de intersección
        normal = subtract_vectors(closest_point, self.position[:2])
        normal = normalize_vector(normal)
        
        # Calcular coordenadas de textura (u, v)
        relative_point = subtract_vectors(closest_point, self.position[:2])
        u = (relative_point[0] / (2 * self.size)) + 0.5
        v = (relative_point[1] / (2 * self.size)) + 0.5
        
        u = max(0, min(0.999, u))
        v = max(0, min(0.999, v))
        
        return Intercept(
            point=[closest_point[0], closest_point[1], orig[2]],  # Volvemos a 3D
            normal=[normal[0], normal[1], 0],  # Normal en 2D, con Z = 0
            distance=min_distance,
            texCoords=[u, v],
            rayDirection=dir,
            obj=self
        )
