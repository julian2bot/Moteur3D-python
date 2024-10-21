import math
import moteur_graphique as mg


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

    def to_screen(self) -> 'Vec2':
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

    def projection(self, focal_lenth: int) -> 'Vec2':
        return focal_lenth * Vec2(self.x, self.y) / self.z

    def rotation_x(self, pitch: int) -> 'Vec3':
        y1 = math.cos(pitch) * self.y - math.sin(pitch) * self.z
        z1 = math.sin(pitch) * self.y + math.cos(pitch) * self.z
        return Vec3(self.x, y1, z1)

    def rotation_y(self, yaw: int) -> 'Vec3':
        x1 = math.cos(yaw) * self.x + math.sin(yaw) * self.z
        z1 = -math.sin(yaw) * self.x + math.cos(yaw) * self.z
        return Vec3(x1, self.y, z1)

    def dot(self: 'Vec3', v2: 'Vec3') -> float:
        # produit scalaire
        return self.x * v2.x + self.y * v2.y + self.z * v2.z

    def line_plane_intersection(self: 'Vec3', plane_point: 'Vec3', v1: 'Vec3',
                                v2: 'Vec3') -> 'Vec3':
        u = v2 - v1
        dotp = self.dot(u)
        if abs(dotp) < 1e-5:
            return (0, 0, 0)
        w = v1 - plane_point
        si = -self.dot(w) / dotp
        u = si * u
        return v1 + u

    def cross_prod(self: 'Vec3', v2: 'Vec3') -> 'Vec3':
        # produit vectoriel
        return Vec3(self.y * v2.z - self.z * v2.y,
                    self.z * v2.x - self.x * v2.z,
                    self.x * v2.y - self.y * v2.x)
    def lenght(self: 'Vec3') -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self: 'Vec3') -> 'Vec3':
        norme = self.lenght()
        return Vec3(self.x / norme, self.y / norme, self.z / norme)


class Triangle2D:

    def __init__(self: 'Triangle2D', v1: Vec2, v2: Vec2, v3: Vec2) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def to_screen(self: 'Triangle2D') -> 'Triangle2D':
        return Triangle2D(self.v1.to_screen(), self.v2.to_screen(),
                          self.v3.to_screen())


class Triangle3D:

    def __init__(self: 'Triangle3D', v1: Vec3, v2: Vec3, v3: Vec3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def projection(self: 'Triangle3D', focal_lenth: int) -> Triangle2D:
        return Triangle2D(self.v1.projection(focal_lenth),
                          self.v2.projection(focal_lenth),
                          self.v3.projection(focal_lenth))

    def translate(self: 'Triangle3D', v: Vec3) -> 'Triangle3D':
        return Triangle3D(self.v1 + v, self.v2 + v, self.v3 + v)

    def rotation_x(self: 'Triangle3D', pitch: int) -> 'Triangle3D':
        return Triangle3D(self.v1.rotation_x(pitch), self.v2.rotation_x(pitch),
                          self.v3.rotation_x(pitch))

    def rotation_y(self: 'Triangle3D', yaw: int) -> 'Triangle3D':
        return Triangle3D(self.v1.rotation_y(yaw), self.v2.rotation_y(yaw),
                          self.v3.rotation_y(yaw))
