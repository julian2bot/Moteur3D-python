import moteur_graphique as mg
import math

from typing import Self

class Vec2:

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __mul__(self, c: int) -> 'Vec2':
        return Vec2(self.x * c, self.y * c)

    def __truediv__(self, c: int) -> 'Vec2':
        return Vec2(self.x / c, self.y / c)

    def __add__(self, v) -> 'Vec2':
        return Vec2(self.x + v.x, self.y + v.y)

    __radd__ = __add__
    __rmul__ = __mul__

    def toScreen(self) -> 'Vec2':
        return Vec2(
            ((29 / 13) * mg.height / mg.width * self.x + 1) * mg.width / 2,
            (-self.y + 1) * mg.height / 2)


class Vec3:

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, c: int) -> 'Vec3':
        return Vec3(self.x * c, self.y * c, self.z * c)

    def __truediv__(self, c: int) -> 'Vec3':
        return Vec3(self.x / c, self.y / c, self.z / c)

    def __add__(self, v) -> 'Vec3':
        return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v) -> 'Vec3':
        return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)

    __radd__ = __add__
    __rmul__ = __mul__

    def projection(self, focalLenth: int) -> 'Vec2':
        return focalLenth * Vec2(self.x, self.y) / self.z

    def rotationX(self, pitch: int) -> 'Vec3':
        y1 = math.cos(pitch) * self.y - math.sin(pitch) * self.z
        z1 = math.sin(pitch) * self.y + math.cos(pitch) * self.z
        return Vec3(self.x, y1, z1)

    def rotationY(self, yaw: int) -> 'Vec3':
        x1 = math.cos(yaw) * self.x - math.sin(yaw) * self.z
        z1 = -math.sin(yaw) * self.x + math.cos(yaw) * self.z
        return Vec3(x1, self.y, z1)
    
    def dot(self:'Vec3', v2:'Vec3'):
        return self.x*v2.x + self.y*v2.y + self.z*v2.z 
    
    def linePlaneIntersection(self, planePoint, v1, v2 ):
        u = v2-v1
        dotp = self.dot(u)
        if abs(dotp)<1e-5:
            return (0,0,0)
        w = (v1 - planePoint)
        si = -self.dot(w)/dotp
        u = si*u
        return v1+u 


class Triangle2D:

    def __init__(self, v1: Vec2, v2: Vec2, v3: Vec2) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def toScreen(self) -> 'Triangle2D':
        return Triangle2D(self.v1.toScreen(), self.v2.toScreen(),
                          self.v3.toScreen())


class Triangle3D:

    def __init__(self, v1: Vec3, v2: Vec3, v3: Vec3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def projection(self, focalLenth: int) -> Triangle2D:
        return Triangle2D(self.v1.projection(focalLenth),
                          self.v2.projection(focalLenth),
                          self.v3.projection(focalLenth))

    def translate(self, v: Vec3) -> 'Triangle3D':
        return Triangle3D(self.v1 + v, self.v2 + v, self.v3 + v)

    def rotationX(self, pitch: int) -> 'Triangle3D':
        return Triangle3D(self.v1.rotationX(pitch), self.v2.rotationX(pitch),
                          self.v3.rotationX(pitch))

    def rotationY(self, yaw: int) -> 'Triangle3D' :
        return Triangle3D(self.v1.rotationY(yaw), self.v2.rotationY(yaw),
                          self.v3.rotationY(yaw))

