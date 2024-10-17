import pygame 
from pygame.locals import *
from gl import *
from figures import *
from material import *
from lights import *
from texture import Texture

width =  64*2*2*2
height = 64*2*2*2
background_color = (0, 0, 0)  

 
screen = pygame.display.set_mode((width,height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture("Raytracer2024/textures/backgrounds/billiard.bmp")


#MATERIALS--------------------------------
#OPAQUE
brick = Material(texture=Texture("Raytracer2024/textures/redrocks.bmp"), diffuse = [0.737,0.290,0.235] , spec = 16 , Ks = 0.5, matType = OPAQUE)
rocks = Material(texture=Texture("Raytracer2024/textures/rocks.bmp"), diffuse = [0.498,0.513,0.525] , spec = 16*2*2 , Ks = 0.2, matType = OPAQUE)
wood = Material(texture=Texture("Raytracer2024/textures/wood.bmp"), diffuse = [0.776,0.635,0.494] , spec = 16*2*2*2 , Ks = 0.5, matType = OPAQUE)
darkwood = Material(texture=Texture("Raytracer2024/textures/darkwood.bmp"), diffuse = [1,1,1] , spec = 16 , Ks = 0.1, matType = OPAQUE)
denim = Material(texture=Texture("Raytracer2024/textures/denim.bmp"), diffuse = [0.776,0.635,0.494] , spec = 16*2*2*2 , Ks = 0.5, matType = OPAQUE)
shirt = Material(texture=Texture("Raytracer2024/textures/shirt.bmp"), diffuse = [0.776,0.635,0.494] , spec = 16*2*2*2 , Ks = 0.5, matType = OPAQUE)
skin = Material(texture=Texture("Raytracer2024/textures/skin.bmp"), diffuse = [0.776,0.635,0.494] , spec = 16*2*2*2 , Ks = 0.5, matType = OPAQUE)

#marmol = Material(texture=Texture("Raytracer2024/textures/marmol.bmp"), diffuse = [1,1,1] , spec = 16*2*2 , Ks = 0.2, matType = OPAQUE)
tierra = Material(texture=Texture("Raytracer2024/textures/tierra.bmp"), diffuse = [1,1,1] , spec = 16*2*2 , Ks = 0.2, matType = OPAQUE)
grass = Material(diffuse = [0.1,1,0.1], spec = 32 , Ks = 0.5)
snow = Material(diffuse = [0.6,0.6,0.6], spec = 63,  Ks = 0.1)
#REFLECTIVE
mirror = Material(diffuse= [0.9,0.9,0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(texture = Texture("Raytracer2024/textures/redrocks.bmp"), spec = 128, Ks = 0.2, matType = REFLECTIVE)
#marble = Material(texture = Texture("Rawytracer2024/textures/marble.bmp"), spec = 128, Ks = 0.2, matType = REFLECTIVE)
#TRANSPARENT
glass = Material(spec = 100, Ks = 0.04, ior = 1.52, matType= TRANSPARENT)
water = Material(spec = 70, Ks = 0.02, ior = 1.33, matType= TRANSPARENT)

#LIGHTS--------------------------------
rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intensity=0.9))
rt.lights.append(AmbientLight(intensity= 0.5))
rt.lights.append(PointLight(position= [0,0,-5],intensity=3))
rt.lights.append(PointLight(position= [0,5,-5],intensity=5))

# #SPHERES--------------------------------
rt.scene.append(Sphere(position=[2.3, 0.3, -4], radius=0.5, material=skin)) #cabeza
rt.scene.append(Sphere(position=[1, -1, -4], radius=0.2, material=skin)) #mano
rt.scene.append(Sphere(position=[3.6, -1, -4], radius=0.2, material=skin)) #mano

rt.scene.append(Sphere(position=[-1.3, -1, -4], radius=0.2, material=grass)) #mano
rt.scene.append(Sphere(position=[-2, -1, -5], radius=0.2, material=snow)) #mano
rt.scene.append(Sphere(position=[-3, -1, -3], radius=0.2, material=brick)) #mano

# #DISKS--------------------------------------
#rt.scene.append(Disk(position= [-5, 1,-9], normal=[0.3,0,1], radius = 0.3, material = mirror))

#AABB---------------------------------------
# pantalon
rt.scene.append(AABB(position = [2.5,-2.01,-4], sizes = [0.5,1,0.35], material = denim)) #ya
rt.scene.append(AABB(position = [2,-2,-4], sizes = [0.4,1,0.35], material = denim))#ya
# camisa
rt.scene.append(AABB(position = [2.25,-0.95,-4], sizes = [1,1.5,0.3], material = shirt)) #camisa

# #TRIANGLE----------------------------------
rt.scene.append(Triangle(v0=[1.7, -0.1, -4], v1=[1.4, -0.3, -4], v2=[1.7, -0.5, -4],  material=shirt)) #sleeve
rt.scene.append(Triangle(v0=[2.9, -0.1, -4], v1=[3.3, -0.3, -4], v2=[2.9, -0.5, -4],  material=shirt))#sleeve

# #CYLINDER-----------------------------------
rt.scene.append(Cylinder(position=[1.55, -0.4, -4], radius=0.13, height=0.8, normal=[-1,0.8,0], material=skin))#brazo
rt.scene.append(Cylinder(position=[3.5, -1, -4], radius=0.13, height=0.8, normal=[1,0.8,0], material=skin)) #brazo

# #
rt.scene.append(Cylinder(position=[1, 0, -5], radius=0.05, height=5, normal=[1,0,0], material=wood)) #palo

#ELLIPSOID----------------------------------
#rt.scene.append(Ellipsoid(position=[1.5, 3.2, -300], radii=[0.2, 0.2, 0.2], material=brick))
# rt.scene.append(Ellipsoid(position=[2, 3.2, -300], radii=[0.2, 0.2, 0.2], material=brick))

#cambiar--------------------------------------
#rt.scene.append(HexagonalPrism(position=[0, 6, -6], radius=0.5, height=1, material=wood))

#rt.scene.append(Star(position=[0, 0, -5], size=2, material=wood))

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
    
rt.glGenerateFrameBuffer("CYLINDER.bmp")
pygame.quit()  
  
