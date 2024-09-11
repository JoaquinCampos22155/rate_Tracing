import pygame 
from pygame.locals import *
from gl import *
from figures import *
from material import *
from lights import *

width =  256
height = 256
background_color = (0, 0, 0)  


screen = pygame.display.set_mode((width,height), pygame.SCALED)
clock = pygame.time.Clock()
 
rt = RendererRT(screen)

brick = Material(diffuse = [1,0,0] , spec = 16 , Ks = 0.05 )
grass = Material(diffuse = [0.1,1,0.1], spec = 32 , Ks = 0.1)
water = Material(diffuse = [0,0,1], spec = 64,  Ks = 0.2)

rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intensity=0.8, color=[1,1,1]))
rt.lights.append(DirectionalLight(direction=[0,0,0], intensity=0.6, color=[1,1,1] ))
rt.lights.append( AmbientLight(intensity= 0.1))

rt.scene.append(Sphere([0, 0, -5], radius= 1, material=brick))
rt.scene.append(Sphere([0.8, 1, -3], radius=0.3, material=grass))
rt.scene.append(Sphere([-0.8, 1, -3], radius=0.3, material=water))




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

pygame.quit()  
  
