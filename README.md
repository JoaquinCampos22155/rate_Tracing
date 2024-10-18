# Raytracer 

Este proyecto implementa un raytracer en tres dimensiones con la capacidad de manejar múltiples figuras geométricas para simular la intersección de rayos con objetos. El raytracer utiliza una librería propia para manejar operaciones vectoriales y cálculos matemáticos.

## Figuras soportadas

El raytracer actual puede manejar las siguientes figuras geométricas:

### 1. **Sphere (Esfera)**
   - Una esfera en 3D definida por su posición y radio.


### 2. **Plane (Plano)**
   - Un plano infinito en 3D definido por su posición y su normal.


### 3. **Disk (Disco)**
   - Un plano circular definido por su radio, posición y normal.


### 4. **AABB (Axis-Aligned Bounding Box)**
   - Una caja alineada con los ejes definida por su posición y tamaño en 3D.


### 5. **Triangle (Triángulo)**
   - Un triángulo en 3D definido por sus tres vértices.


### 6. **Cylinder (Cilindro)**
   - Un cilindro en 3D definido por su posición, radio, altura y normal.


### 7. **Ellipsoid (Elipsoide)**
   - Un elipsoide definido por sus radios en los tres ejes.

### 8. **HexagonalPrism (Prisma Hexagonal)**
   - Un prisma hexagonal en 3D definido por su posición, radio y altura.


### 9. **Star (Estrella)
   - Una figura de estrella de cinco picos en 2D con alternancia entre puntos interiores y exteriores.


## Requisitos

Este proyecto depende de una librería personalizada para operaciones vectoriales (`Mathlib`) y la clase `Intercept` que maneja los resultados de la intersección. Asegúrate de tener estas dependencias configuradas correctamente.
