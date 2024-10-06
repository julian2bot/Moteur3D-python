import moteur_graphique as mg
from lib_math import *
import constante as const
import keyboard
import time


import meshio

mesh = meshio.read("rectangle.stl")  # or .off, .vtk, .ply, ...
# mesh.points, mesh.cells, ...


# tri = Triangle3D(Vec3(-0.5, -0.5, 1.5), Vec3(0, 0.5, 1.5),
#                  Vec3(0.5, -0.5, 1.5))

carre = [
    Triangle3D(Vec3(-0.5, -0.5, 1), Vec3(-0.5, 0.5, 1), Vec3(0.5, 0.5, 1)),
    Triangle3D(Vec3(-0.5, -0.5, 2), Vec3(0.5, 0.5, 1), Vec3(0.5, -0.5, 1))
]


import numpy as np
points = np.array(mesh.points)
min_vals = points.min(axis=0)
max_vals = points.max(axis=0)
def normalize_point(point, min_vals, max_vals):
    return 2 * ((point - min_vals) / (max_vals - min_vals)) - 1
normalized_points = np.array([normalize_point(point, min_vals, max_vals) for point in mesh.points])

forme = []
for triangle in mesh.cells[0].data:

    p1 = normalized_points[triangle[0]]  
    p2 = normalized_points[triangle[1]]  
    p3 = normalized_points[triangle[2]] 

    forme.append(Triangle3D(Vec3(p1[const.X],p1[const.Y],p1[const.Z]), Vec3(p2[const.X],p2[const.Y],p2[const.Z]), Vec3(p3[const.X],p3[const.Y],p3[const.Z])))



cam = mg.Camera(Vec3(0, 0, 0), 0, 0)


def inputs(dt: float):
    if keyboard.is_pressed("down arrow"):
        if cam.pitch > -const.PI_SUR_DEUX:
            cam.pitch -= const.DEFAULT_DEPLACEMENT * dt
    if keyboard.is_pressed("up arrow"):
        if cam.pitch < const.PI_SUR_DEUX:
            cam.pitch += const.DEFAULT_DEPLACEMENT * dt

    if keyboard.is_pressed("left arrow"):
        cam.yaw += const.DEFAULT_DEPLACEMENT * dt
    if keyboard.is_pressed("right arrow"):
        cam.yaw -= const.DEFAULT_DEPLACEMENT * dt

    if keyboard.is_pressed("z"):
        cam.position += cam.getForwardDirection(
        ) * const.DEFAULT_DEPLACEMENT * dt
    if keyboard.is_pressed("s"):
        cam.position += -1 * cam.getForwardDirection(
        ) * const.DEFAULT_DEPLACEMENT * dt

    if keyboard.is_pressed("d"):
        cam.position += cam.getRightDirection(
        ) * const.DEFAULT_DEPLACEMENT * dt
    if keyboard.is_pressed("q"):
        cam.position += -1 * cam.getRightDirection(
        ) * const.DEFAULT_DEPLACEMENT * dt

    if keyboard.is_pressed("space"):
        cam.position.y += const.DEFAULT_DEPLACEMENT * dt
    if keyboard.is_pressed("shift"):
        cam.position.y -= const.DEFAULT_DEPLACEMENT * dt


dernier = 0

while True:
    
    temps_actuelle = time.time()
    dt = (temps_actuelle - dernier) * 100
    dernier = temps_actuelle

    mg.clear(const.BACKGROUND)

    inputs(dt)

    # mg.putMesh(forme, cam, const.DEFAULT_CHAR)
    mg.putMesh(carre, cam, const.DEFAULT_CHAR)
    mg.draw()

input()
