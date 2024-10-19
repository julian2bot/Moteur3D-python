import os
from lib_math import *
import constante as const
from camera import Camera

width, height = os.get_terminal_size()
height -= 1

pixelBuffer = [const.BACKGROUND] * (width * height)


def draw() -> None:
    print(''.join(pixelBuffer), end="")


def clear(char: str) -> None:
    for i in range(width * height):
        pixelBuffer[i] = char


def putPixel(V: Vec2, char: str) -> None:
    px = round(V.x)
    py = round(V.y)
    if (0 <= px <= width and 0 <= py <= height):
        pixelBuffer[py * width + px] = char


def putTriangle(tri: Triangle3D, char: str) -> None:

    def E(p: Vec2, a: Vec2, b: Vec2) -> int:
        return (a.x - p.x) * (b.y - p.y) - (a.y - p.y) * (b.x - p.x)

    def est_dans_le_triangle(v1: Vec2, v2: Vec2, v3: Vec2, p: Vec2) -> bool:
        return E(v3, v1, p) > 0 and E(v2, v3, p) > 0 and E(v1, v2, p) > 0 or E(
            v3, v1, p) < 0 and E(v2, v3, p) < 0 and E(v1, v2, p) < 0

    xmin = round(min(tri.v1.x, tri.v2.x, tri.v3.x))
    xmax = round(max(tri.v1.x, tri.v2.x, tri.v3.x) + 1)
    ymin = round(min(tri.v1.y, tri.v2.y, tri.v3.y))
    ymax = round(max(tri.v1.y, tri.v2.y, tri.v3.y) + 1)

    for y in range(ymin, ymax):
        if 0 <= y < height:
            for x in range(xmin, xmax):
                if 0 <= x < width:
                    pos = Vec2(x, y)

                    if (est_dans_le_triangle(tri.v1, tri.v2, tri.v3, pos)):
                        putPixel(pos, char)

def clip( triangle, camPos, planeNormal):
    def inZ(planeNormal,planePoint, tri ):
        out = [] 
        inT = [] 

        vert1 = planeNormal.dot(planePoint-tri.v1)
        vert2 = planeNormal.dot(planePoint-tri.v2)
        vert3 = planeNormal.dot(planePoint-tri.v3)

        out.append(tri.v1) if vert1>0 else inT.append(tri.v1)
        out.append(tri.v2) if vert2>0 else inT.append(tri.v2)
        out.append(tri.v3) if vert3>0 else inT.append(tri.v3)

        return out, inT
    
    zNear = camPos + 0.1*planeNormal
    out, in_ = inZ(planeNormal,zNear, triangle)

    if(len(out)==0):
        return [triangle]
    elif (len(out)== 3):
        return []
    elif len(out)== 1:
        collision0 = planeNormal.linePlaneIntersection(zNear, out[0], in_[0])
        collision1 = planeNormal.linePlaneIntersection(zNear, out[0], in_[1])
        return [
            Triangle3D(collision0, in_[0], collision1),
            Triangle3D(collision1, in_[0], in_[1])
        ]

    elif len(out)== 2:
        collision0 = planeNormal.linePlaneIntersection(zNear, out[0], in_[0])
        collision1 = planeNormal.linePlaneIntersection(zNear, out[1], in_[0])

        return [
            Triangle3D(collision0, collision1, in_[0]),
        ]






def putMesh(mesh: list[Triangle3D], cam: Camera, char: str) -> None:
    
    lookAt = cam.getLookAtDirection()

    for triangle in mesh:
        clippedTriangleList = clip(triangle, cam.position, lookAt)
        
        for clippedTriangle in clippedTriangleList:
            putTriangle(
                clippedTriangle
                .translate(-1*cam.position)
                .rotationY(cam.yaw)
                .rotationX(cam.pitch)
                .projection(cam.focalLenth)
                .toScreen(),
                 char)
