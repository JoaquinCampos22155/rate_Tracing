import pygame 
from pygame.locals import *
from gl import *
from figures import *
from material import *
from lights import *

width =  128*2*2
height = 128*2*2
background_color = (0, 0, 0)  


screen = pygame.display.set_mode((width,height), pygame.SCALED)
clock = pygame.time.Clock()
 
rt = RendererRT(screen)

brick = Material(diffuse = [1,0,0] , spec = 16 , Ks = 0.5)
grass = Material(diffuse = [0.1,1,0.1], spec = 32 , Ks = 0.5)
water = Material(diffuse = [0,0,1], spec = 128,  Ks = 0.2)
#materiales lab 1
snow = Material(diffuse = [0.6,0.6,0.6], spec = 63,  Ks = 0.1)
eyewhite = Material(diffuse = [1,1,1], spec = 128,  Ks = 1)
eyes = Material(diffuse = [0,0,0], spec = 256,  Ks = 0.9)
nose = Material(diffuse = [1,0.4,0], spec = 128,  Ks = 0.9)
mouth = Material(diffuse = [0,0,0], spec = 128,  Ks = 0.9)
buttons = Material(diffuse = [0,0,0], spec = 256,  Ks = 0.1)




rt.lights.append(DirectionalLight(direction=[-1,-1,-1], intensity=0.8, color=[1,1,1]))

rt.lights.append(AmbientLight(intensity= 1))

#cuerpo
rt.scene.append(Sphere([0, -0.5, -4], radius= 0.7, material=snow))
rt.scene.append(Sphere([0, 0.4, -3.9], radius=0.45, material=snow))
rt.scene.append(Sphere([0, 1, -3.89], radius= 0.32, material=snow))
#ojos
rt.scene.append(Sphere([0.095, 0.82, -2.81], radius= 0.045, material=eyewhite))
rt.scene.append(Sphere([-0.095, 0.82, -2.81], radius= 0.045, material=eyewhite))
rt.scene.append(Sphere([-0.09, 0.80, -2.7], radius= 0.03, material=eyes))
rt.scene.append(Sphere([0.09, 0.80, -2.7], radius= 0.03, material=eyes))
#nariz
rt.scene.append(Sphere([0, 0.73, -2.7], radius= 0.050, material=nose))
#boca
rt.scene.append(Sphere([-0.09, 0.57, -2.3], radius= 0.01, material=mouth))
rt.scene.append(Sphere([0.09, 0.57, -2.3], radius= 0.01, material=mouth))
rt.scene.append(Sphere([-0.05, 0.55, -2.3], radius= 0.01, material=mouth))
rt.scene.append(Sphere([0.05, 0.55, -2.3], radius= 0.01, material=mouth))
rt.scene.append(Sphere([0, 0.54, -2.3], radius= 0.01, material=mouth))
#botones
rt.scene.append(Sphere([0, 0.3, -2.5], radius= 0.05, material=buttons))
rt.scene.append(Sphere([0, 0.05, -2.5], radius= 0.06, material=buttons))
rt.scene.append(Sphere([0, -0.3, -2.5], radius= 0.07, material=buttons))







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
  
