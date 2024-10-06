import moteur_graphique as mg
from lib_math import *
import constante as const
import keyboard
import time

tri = Triangle3D(Vec3(-0.5, -0.5, 1.5), Vec3(0, 0.5, 1.5),
                 Vec3(0.5, -0.5, 1.5))

carre = [
    Triangle3D(Vec3(-0.5, -0.5, 1), Vec3(-0.5, 0.5, 1), Vec3(0.5, 0.5, 1)),
    Triangle3D(Vec3(-0.5, -0.5, 2), Vec3(0.5, 0.5, 1), Vec3(0.5, -0.5, 1))
]

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

    mg.putMesh(carre, cam, const.DEFAULT_CHAR)
    mg.draw()

input()
