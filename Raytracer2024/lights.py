from  Mathlib import *
from math import cos, pi
import numpy as np
class Light(object):
    def __init__(self, color = [1,1,1], intensity = 1.0, lightType = "None"):
        self.color = color 
        self.intensity = intensity
        self.lightType = lightType
    def GetLightColor(self, intercept = None):
        return [(i * self.intensity) for i in self.color]
    
    def GetSpecularColor(self, intercept, viewPos):
        return [0,0,0]
        

class AmbientLight(Light):
    def __init__(self, color = [1,1,1], intensity = 1.0):
        super().__init__(color, intensity, "Ambient")

class DirectionalLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1, direction = [0,1,0]):
        super().__init__(color, intensity, "Directional")
        self.direction = normalize_vector(direction)
        
    def GetLightColor(self, intercept = None):
        lightColor =  super().GetLightColor()
        
        if intercept:
            dir = [(i * -1) for i in self.direction]
            intensity = dotProd(intercept.normal, dir)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)
            lightColor = [(i * intensity) for i in lightColor]
            
        return lightColor
    
    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color 
        if intercept:
            dir = [(i*-1) for i in self.direction]
            reflect = reflectVector(intercept.normal, dir)
            
            viewDir = [viewPos[i] - intercept.point[i] for i in range(3)]
            viewDir = normalize_vector(viewDir)

            #specular = ((V . R) ^ n) * Ks
            specularity = max(0,dotProd(viewDir, reflect)) ** intercept.obj.material.spec      
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity

            specColor = [(i*specularity) for i in specColor]

        return specColor
    
    
    
class PointLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1, position = [0,0,0] ,):
        super().__init__(color, intensity)
        self.position = position
        self.lightType = "Point"
        
    def GetLightColor(self, intercept = None):
        lightColor =  super().GetLightColor(intercept)
        
        if intercept:
            dir = np.subtract(self.position, intercept.point)
            #np.linalg.norm() magnitud de vector
            R = np.linalg.norm(dir)
            dir /= R
            
            intensity = np.dot(intercept.normal, dir)
            intensity = max(0, min(1, intensity))
            intensity *= (1- intercept.obj.material.Ks)
            
            # ley de cuadrados inversos
            # attenuation = intensity / R^2
            # R es la distancia del punto intercepto a la luz punto
            
            if R != 0:
                intensity /= R**2

            lightColor = [(i * intensity) for i in lightColor]
            
        return lightColor
    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color 
        if intercept:
            dir = np.subtract(self.position, intercept.point)
            #np.linalg.norm() magnitud de vector
            R = np.linalg.norm(dir)
            dir /= R
            
            reflect = reflectVector(intercept.normal, dir)
            
            viewDir = [viewPos[i] - intercept.point[i] for i in range(3)]
            viewDir = normalize_vector(viewDir)

            #specular = ((V . R) ^ n) * Ks
            specularity = max(0,dotProd(viewDir, reflect)) ** intercept.obj.material.spec      
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity

            if R != 0:
                specularity /= R**2

            specColor = [(i*specularity) for i in specColor]
        return specColor    
    
class SpotLight(PointLight):
    def __init__(self, color=[1, 1, 1], intensity=1, position=[0, 0, 0], direction = [0,-1,0], innerAngle = 50, outerAngle = 60):
        super().__init__(color, intensity, position)
        self.direction = direction
        self.innerAngle = innerAngle
        self.outerAngle = outerAngle
        self.lightType = "Spot"
        
    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor(intercept)
        
        if intercept:
            lightColor = [i*self.SpotLightAttenuation(intercept) for i in lightColor]
        return lightColor
    def GetSpecularColor(self, intercept, viewPos):
        specularColor = super().GetSpecularColor(intercept, viewPos)
        if intercept:
            specularColor = [i*self.SpotLightAttenuation(intercept) for i in specularColor]
        return specularColor
    def SpotLightAttenuation(self, intercept = None):
        if intercept == None:
            return 0
        wi = np.subtract(self.position, intercept.point)
        wi /= np.linalg.norm(wi)
        
        innerAngleRads = self.innerAngle *pi /180
        outerAngleRads = self.outerAngle *pi /180
        
        attenuation = (-np.dot(self.direction, wi) - cos(outerAngleRads) ) /(cos(innerAngleRads) - cos(outerAngleRads))
        
        attenuation = min(1, max(0, attenuation))
        
        return attenuation