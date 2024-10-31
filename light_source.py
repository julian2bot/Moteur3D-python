"""
Source de lumiere
"""
from constante import LIGHT_GRADIENT
from lib_math import Vec3


class LightSource:
    """
        Source de lumière à une position donnée
    """
    def __init__(self: 'LightSource', position: Vec3) -> None:
        """
            Création d'une lumière à une position donnée

        Args:
            self (LightSource): Lumiere
            position (Vec3): Position de la source de lumière
        """
        self.position = position

    def diffuse_light(self: 'LightSource', normal: Vec3, v: Vec3) -> str:
        """ 
            Renvoie le caractère qui correspond au mieux à l'intensité lumineuse.

        Args:
            self (LightSource): Lumiere
            normal (Vec3): Surface normal
            v (Vec3): Notre triangle

        Returns:
            str: Caractère pour simuler la luminosité dans la chaîne de caractère 
                LIGHT_GRIENT qui est une chaîne de caractères de 
                    peu lumineux a plus lumineux 
        """
        light_direction = self.position - v
        intensity = light_direction.normalize().dot(
            normal.normalize())  # valeur entre -1 et 1

        return LIGHT_GRADIENT[round(
            intensity * (len(LIGHT_GRADIENT) -
                         1))] if intensity >= 0 else LIGHT_GRADIENT[0]

    def move(self: 'LightSource', dt: float) -> None:
        """
            Faire bouger la lumière
        """
        self.position.z -= dt / 100
