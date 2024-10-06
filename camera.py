import math
from lib_math import *


class Camera:

    def __init__(self,
                 position: Vec3,
                 pitch: float,
                 yaw: float,
                 focalLenth: int = 1) -> None:
        self.position = position
        self.pitch = pitch
        self.yaw = yaw
        self.focalLenth = focalLenth

    def getLookAtDirection(self):
        pass

    def getForwardDirection(self) -> Vec3:
        return Vec3(-math.sin(self.yaw), 0, math.cos(self.yaw))

    def getRightDirection(self)-> Vec3:
        return Vec3(math.cos(self.yaw), 0, math.sin(self.yaw))
