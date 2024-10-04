import pygame 
from pygame.locals import *
from gl import *
from figures import *
from material import *
from lights import *
from texture import Texture

width =  64*2
height = 64*2
background_color = (0, 0, 0)  

 
screen = pygame.display.set_mode((width,height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("Raytracer2024/textures/backgrounds/squashcourt.bmp")


#MATERIALS--------------------------------
#OPAQUE
brick = Material(texture=Texture("Raytracer2024/textures/redrocks.bmp"), diffuse = [0.737,0.290,0.235] , spec = 16 , Ks = 0.5, matType = OPAQUE)
rocks = Material(texture=Texture("Raytracer2024/textures/rocks.bmp"), diffuse = [0.498,0.513,0.525] , spec = 16*2*2 , Ks = 0.2, matType = OPAQUE)
wood = Material(texture=Texture("Raytracer2024/textures/wood.bmp"), diffuse = [0.776,0.635,0.494] , spec = 16*2*2*2 , Ks = 0.5, matType = OPAQUE)
darkwood = Material(texture=Texture("Raytracer2024/textures/darkwood.bmp"), diffuse = [1,1,1] , spec = 16 , Ks = 0.1, matType = OPAQUE)
marmol = Material(texture=Texture("Raytracer2024/textures/marmol.bmp"), diffuse = [1,1,1] , spec = 16*2*2 , Ks = 0.2, matType = OPAQUE)
tierra = Material(texture=Texture("Raytracer2024/textures/tierra.bmp"), diffuse = [1,1,1] , spec = 16*2*2 , Ks = 0.2, matType = OPAQUE)
grass = Material(diffuse = [0.1,1,0.1], spec = 32 , Ks = 0.5)
water = Material(diffuse = [0,0,1], spec = 128,  Ks = 0.2)
snow = Material(diffuse = [0.6,0.6,0.6], spec = 63,  Ks = 0.1)
#REFLECTIVE
mirror = Material(diffuse= [0.9,0.9,0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(texture = Texture("Raytracer2024/textures/redrocks.bmp"),diffuse= [0.5,0.5,1.0], spec = 128, Ks = 0.2, matType = REFLECTIVE)
bkgroundmirror = Material(texture = Texture("Raytracer2024/textures/redrocks.bmp"), spec = 128, Ks = 0.2, matType = REFLECTIVE)
#marble = Material(texture = Texture("Raytracer2024/textures/whiteMarble.bmp"), spec = 128, Ks = 0.2, matType = REFLECTIVE)
#TRANSPARENT
glass = Material(spec = 123, Ks = 0.2, ior = 1.5, matType= TRANSPARENT)

#LIGHTS--------------------------------
rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intensity=0.9))
rt.lights.append(AmbientLight(intensity= 0.5))
rt.lights.append(PointLight(position= [0,0,-5],intensity=3))

#SPHERES--------------------------------
#rt.scene.append(Sphere([-1, 0, -6], radius=0.5, material=brick))
# rt.scene.append(Sphere([-1.5, -1, -5], radius=0.5, material=rocks))
# rt.scene.append(Sphere([0, 1, -7], radius=0.5, material=mirror))
# rt.scene.append(Sphere([0, -1, -7], radius=0.5, material=blueMirror))
# rt.scene.append(Sphere([1.5, 1, -5], radius=0.5, material=glass))
# rt.scene.append(Sphere([1.5, -1, -5], radius=0.5, material=glass))
#rt.scene.append(Sphere([0, 0, -5], radius=1.5, material=glass))

#PLANES---------------------------------
# #rt.scene.append(Plane(position=[0,0,-5], normal=[0,-1,-2], material=wood))
# rt.scene.append(Plane(position=[0,2,0], normal=[0,-1,0], material=brick))  # Techo
# rt.scene.append(Plane(position=[0,-2,0], normal=[0,1,0], material=tierra))  # Piso
# rt.scene.append(Plane(position=[-3,0,-10], normal=[1,0,0], material=marmol))  # Pared izquierda
# rt.scene.append(Plane(position=[3,0,-10], normal=[-1,0,0], material=marmol))  # Pared derecha
# rt.scene.append(Plane(position=[0,0,-10], normal=[0,0,1], material=water))  # Pared de fondo


# rt.scene.append(Plane(position=[2,0,-10], normal=[1,0,0], material=wood))
# rt.scene.append(Plane(position=[-2,0,-10], normal=[-1,0,0], material=wood))

#DISKS----------------------------------
# rt.scene.append(Disk(position= [0,0,-9], normal=[0,0,1], radius = 1, material = mirror))

#AABB----------------------------------
# rt.scene.append(AABB(position = [-1,0,-4], sizes = [0.7,0.7,0.7], material = wood))
# rt.scene.append(AABB(position = [1,0,-4], sizes = [0.7,0.7,0.7], material = brick))

#TRIANGLE----------------------------------
rt.scene.append(Triangle(v0=[-1, 0, -4], v1=[-0.3, 1, -4], v2=[-1.7, 1, -4],  material=wood))



rt.glRender()


isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
           
    pygame.display.flip()	  
    clock.tick(60)
    
rt.glGenerateFrameBuffer("HIGHR.bmp")
pygame.quit()  
  
