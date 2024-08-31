
class Material(object):
    def __init__(self, diffuse):
        self.diffuse = diffuse
    
    def GetSurfaceColor(self, intercept, renderer):
        # Phong reflection model 
        # LightColor = LightColor + Specular
        # FinalCOlor = DiffuseColor * LightColor
        
        lightColor = [0,0,0]
        finalColor = self.diffuse
        
        for light in renderer.lights:
            currentLightColor = light.GetLightColor(intercept)
            lightColor = [(lightColor[i] + currentLightColor[i]) for i in range(3)]
        finalColor = [(finalColor[i] * lightColor[i]) for i in range(3)]
        finalColor = [min(1, finalColor[i])for i in range(3)]
        
        return finalColor