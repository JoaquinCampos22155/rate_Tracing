import pygame 
from pygame.locals import *
from gl import *
from figures import *

width = 512
height = 512 
background_color = (0, 0, 0)  


screen = pygame.display.set_mode((width,height), pygame.SCALED)
clock = pygame.time.Clock()

rt = RendererRT(screen)

rt.scene.append(Sphere([0, 0, -5], 1))

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
  
