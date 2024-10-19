import os
from lib_math import *
import constante as const
from camera import Camera
from lightSource import LightSource

width, height = os.get_terminal_size()
height -= 1


class Moteur_Graphique:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixelBuffer = [const.BACKGROUND] * (width * height)

    def draw(self: 'Moteur_Graphique') -> None:
        print(''.join(self.pixelBuffer), end="")

    def clear(self: 'Moteur_Graphique', char: str) -> None:
        for i in range(self.width * self.height):
            self.pixelBuffer[i] = char

    def putPixel(self: 'Moteur_Graphique', V: Vec2, char: str) -> None:
        px = round(V.x)
        py = round(V.y)
        if (0 <= px <= self.width and 0 <= py <= self.height):
            self.pixelBuffer[py * self.width + px] = char

    def putTriangle(self: 'Moteur_Graphique', tri: Triangle3D,
                    char: str) -> None:

        def E(p: Vec2, a: Vec2, b: Vec2) -> int:
            return (a.x - p.x) * (b.y - p.y) - (a.y - p.y) * (b.x - p.x)

        def est_dans_le_triangle(v1: Vec2, v2: Vec2, v3: Vec2,
                                 p: Vec2) -> bool:
            return E(v3, v1, p) > 0 and E(v2, v3, p) > 0 and E(
                v1, v2, p) > 0 or E(v3, v1, p) < 0 and E(v2, v3, p) < 0 and E(
                    v1, v2, p) < 0

        xmin = round(min(tri.v1.x, tri.v2.x, tri.v3.x))
        xmax = round(max(tri.v1.x, tri.v2.x, tri.v3.x) + 1)
        ymin = round(min(tri.v1.y, tri.v2.y, tri.v3.y))
        ymax = round(max(tri.v1.y, tri.v2.y, tri.v3.y) + 1)

        for y in range(ymin, ymax):
            if 0 <= y < self.height:
                for x in range(xmin, xmax):
                    if 0 <= x < self.width:
                        pos = Vec2(x, y)

                        if (est_dans_le_triangle(tri.v1, tri.v2, tri.v3, pos)):
                            self.putPixel(pos, char)

    def clip(self: 'Moteur_Graphique', triangle: Triangle3D, camPos: Vec3,
             planeNormal: Vec3) -> list[Triangle3D]:

        def inZ(planeNormal: Vec3, planePoint: Vec3,
                tri: Triangle3D) -> tuple[list[Vec3], list[Vec3], bool]:

            out = []
            inT = []

            vert1 = planeNormal.dot(planePoint - tri.v1)
            vert2 = planeNormal.dot(planePoint - tri.v2)
            vert3 = planeNormal.dot(planePoint - tri.v3)

            out.append(tri.v1) if vert1 > 0 else inT.append(tri.v1)
            out.append(tri.v2) if vert2 > 0 else inT.append(tri.v2)
            out.append(tri.v3) if vert3 > 0 else inT.append(tri.v3)

            return out, inT, vert1 * vert2 > 0

        zNear = camPos + 0.1 * planeNormal
        out, in_, isInverted = inZ(planeNormal, zNear, triangle)

        if (len(out) == 0):
            return [triangle]
        elif (len(out) == 3):
            return []
        elif len(out) == 1:
            collision0 = planeNormal.linePlaneIntersection(
                zNear, out[0], in_[0])
            collision1 = planeNormal.linePlaneIntersection(
                zNear, out[0], in_[1])
            if isInverted:
                return [
                    Triangle3D(collision1, in_[1], collision0),
                    Triangle3D(collision0, in_[1], in_[0])
                ]
            else:
                return [
                    Triangle3D(collision0, in_[0], collision1),
                    Triangle3D(collision1, in_[0], in_[1])
                ]

        elif len(out) == 2:
            collision0 = planeNormal.linePlaneIntersection(
                zNear, out[0], in_[0])
            collision1 = planeNormal.linePlaneIntersection(
                zNear, out[1], in_[0])

            if isInverted:
                return [
                    Triangle3D(collision0, in_[0], collision1),
                ]
            else:
                return [
                    Triangle3D(collision0, collision1, in_[0]),
                ]

    def putMesh(self: 'Moteur_Graphique', mesh: list[Triangle3D], cam: Camera,
                lightSource: LightSource) -> None:

        lookAt = cam.get_look_at_direction()

        for triangle in mesh:
            clippedTriangleList = self.clip(triangle, cam.position, lookAt)

            for clippedTriangle in clippedTriangleList:
                line1 = clippedTriangle.v2 - clippedTriangle.v1
                line2 = clippedTriangle.v3 - clippedTriangle.v1
                surfaceNormal = line1.crossProd(line2)

                if surfaceNormal.dot(clippedTriangle.v1 - cam.position) < 0:
                    lightStr: str = lightSource.diffuseLight(
                        surfaceNormal, clippedTriangle.v1)
                    self.putTriangle(
                        clippedTriangle.translate(-1 * cam.position).rotationY(
                            cam.yaw).rotationX(cam.pitch).projection(
                                cam.focal_lenth).toScreen(), lightStr)
