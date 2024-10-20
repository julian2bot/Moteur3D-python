from constante import LIGHT_GRADIENT
from lib_math import Vec3


class LightSource:

    def __init__(self: 'LightSource', position: Vec3) -> None:
        self.position = position

    def diffuse_light(self: 'LightSource', normal: Vec3, v: Vec3) -> str:
        light_direction = self.position - v
        intensity = light_direction.normalize().dot(normal.normalize())
        return LIGHT_GRADIENT[round(
            intensity * (len(LIGHT_GRADIENT) -
                         1))] if intensity >= 0 else LIGHT_GRADIENT[0]
