import pygame 
from pygame.locals import *
from gl import *
from figures import *
from material import *
from lights import *
from texture import Texture

width =  128/2/2
height = 128/2/2
background_color = (0, 0, 0)  


screen = pygame.display.set_mode((width,height), pygame.SCALED)
clock = pygame.time.Clock()
 
rt = RendererRT(screen)
rt.envMap = Texture("Raytracer2024/textures/parkingLot.bmp")


#MATERIALS--------------------------------
#OPAQUE
brick = Material(diffuse = [1,0,0] , spec = 16 , Ks = 0.5)
grass = Material(diffuse = [0.1,1,0.1], spec = 32 , Ks = 0.5)
water = Material(diffuse = [0,0,1], spec = 128,  Ks = 0.2)
snow = Material(diffuse = [0.6,0.6,0.6], spec = 63,  Ks = 0.1)
eyewhite = Material(diffuse = [1,1,1], spec = 128,  Ks = 1)
eyes = Material(diffuse = [0,0,0], spec = 256,  Ks = 0.9)
nose = Material(diffuse = [1,0.4,0], spec = 128,  Ks = 0.9)
mouth = Material(diffuse = [0,0,0], spec = 128,  Ks = 0.9)
buttons = Material(diffuse = [0,0,0], spec = 256,  Ks = 0.1)
#REFLECTIVE
mirror = Material(diffuse= [0.9,0.9,0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(diffuse= [0.5,0.5,1.0], spec = 128, Ks = 0.2, matType = REFLECTIVE)
bkground = Material(texture = Texture("Raytracer2024/textures/parkingLot.bmp"))
#marble = Material(texture = Texture("Raytracer2024/textures/whiteMarble.bmp"), spec = 128, Ks = 0.2, matType = REFLECTIVE)
#TRANSPARENT
glass = Material(spec = 123, Ks = 0.2, ior = 1.5, matType= TRANSPARENT)

#LIGHTS--------------------------------
rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intensity=0.8))
rt.lights.append(AmbientLight(intensity= 0.1))

#SPHERES--------------------------------
rt.scene.append(Sphere([0, 0, -5], radius=1.5, material=glass))


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
    
rt.glGFB("HIGHR.bmp")
pygame.quit()  
  
