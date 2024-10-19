from constante import LIGHT_GRADIENT
from lib_math import Vec3


class LightSource:

    def __init__(self: 'LightSource', position: Vec3) -> None:
        self.position = position

    def diffuseLight(self: 'LightSource', normal: Vec3, v: Vec3) -> str:
        lightDir = self.position - v
        intensity = lightDir.normalize().dot(normal.normalize())
        return LIGHT_GRADIENT[round(
            intensity * (len(LIGHT_GRADIENT) -
                         1))] if intensity >= 0 else LIGHT_GRADIENT[0]
