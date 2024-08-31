import pygame 
from pygame.locals import *
from gl import *
from figures import *
from material import *
from lights import *

width = 200
height = 200 
background_color = (0, 0, 0)  


screen = pygame.display.set_mode((width,height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)

brick = Material(diffuse = [1,0,0] )
grass = Material(diffuse = [0.1,1,0.1] )
water = Material(diffuse = [0,0,1] )

rt.lights.append(DirectionalLight(direction=[-1,-1,-1]))
#rt.lights.append( AmbientLight(intensity=))

rt.scene.append(Sphere([0, 0, -5], 1, brick))
rt.scene.append(Sphere([0.8, 1, -5], 0.8, grass))
rt.scene.append(Sphere([-0.8, 1, -5], 0.8, water))


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
  
