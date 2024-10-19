import moteur_graphique as mg
from lib_math import *
import constante as const
import keyboard
import time
import loader
from pynput.mouse import Listener


# tri = Triangle3D(Vec3(-0.5, -0.5, 1.5), Vec3(0, 0.5, 1.5),
#                  Vec3(0.5, -0.5, 1.5))

carre = [
    Triangle3D(Vec3(-0.5, -0.5, 1), Vec3(-0.5, 0.5, 1), Vec3(0.5, 0.5, 1)),
    Triangle3D(Vec3(-0.5, -0.5, 1), Vec3(0.5, 0.5, 1), Vec3(0.5, -0.5, 1))
]

llight= mg.LightSource(Vec3(0,20,0))

cam = mg.Camera(Vec3(0, 0,-2), 0, -2.0)

mouse_dx = 0
mouse_dy = 0

def on_move(x, y):
    global mouse_dx, mouse_dy
    mouse_dx = x  # pos x de la souris
    mouse_dy = y  # pos y de la souris

listener = Listener(on_move=on_move)
listener.start()

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

    # if keyboard.is_pressed("a"):
    #     cam.focalLenth += .1 * dt
    # if keyboard.is_pressed("e"):
    #     cam.focalLenth -= .1 * dt

    if keyboard.is_pressed("c"):
        exit()


dernier = 0
def camMove(prev_mouse_x, prev_mouse_y, mouse_dx, mouse_dy):
    delta_x = mouse_dx - prev_mouse_x
    delta_y = mouse_dy - prev_mouse_y
    cam.yaw -= delta_x * const.DEFAULT_DEPLACEMENT / 2 * dt
    cam.pitch -= delta_y * const.DEFAULT_DEPLACEMENT / 3 * dt    
    prev_mouse_x = mouse_dx
    prev_mouse_y = mouse_dy
    return prev_mouse_x, prev_mouse_y 

prev_mouse_x, prev_mouse_y = mouse_dx, mouse_dy

load = loader.Loader()
cube = load.loadObj("cube.obj")

while True:
    fps = 40
    # time.sleep(0.01)

    temps_actuelle = time.time()
    dt = (temps_actuelle - dernier) * 100
    dernier = temps_actuelle
    mg.clear(const.BACKGROUND)
    inputs(dt)
    prev_mouse_x, prev_mouse_y = camMove(prev_mouse_x, prev_mouse_y, mouse_dx, mouse_dy)

    # mg.putMesh(forme, cam, const.DEFAULT_CHAR)
    # mg.putMesh(carre, cam,llight)
    mg.putMesh(cube, cam,llight)
    mg.draw()

input()
