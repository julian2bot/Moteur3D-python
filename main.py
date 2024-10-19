import os
import moteur_graphique as mg
from lib_math import *
import constante as const
import time
import loader
from pynput.mouse import Listener

class Main:

    def __init__(self:'Main', MoteurGraphique:mg.Moteur_Graphique, cam: mg.Camera, light:mg.LightSource)->None:
        self.moteur_graphique = MoteurGraphique
        self.cam = cam
        self.dernier = 0
        self.light = light
        # souris a faire
        self.listener = Listener(on_move=self.cam.on_move)

        self.mouse_dx = 0
        self.mouse_dy = 0
        self.prev_mouse_x, self.prev_mouse_y = self.mouse_dx, self.mouse_dy

        
    def lunch(self: 'Main') -> None:
        # souris a faire

        # listener = Listener(on_move=self.cam.on_move)
        # listener.start()
        self.listener.start()
        while True:
            # time.sleep(0.01)

            temps_actuelle = time.time()
            dt = (temps_actuelle - self.dernier) * 100
            self.dernier = temps_actuelle
            self.moteur_graphique.clear(const.BACKGROUND)
            cam.inputs(dt)
            # souris a faire
            cam.prev_mouse_x, cam.prev_mouse_y = self.cam.cam_move(cam.prev_mouse_x, cam.prev_mouse_y, cam.mouse_dx, cam.mouse_dy, dt)

            self.moteur_graphique.putMesh(cube, cam, self.light)
            self.moteur_graphique.draw()






if __name__ == "__main__":

    MoteurGraphique = mg.Moteur_Graphique(mg.width, mg.height)

    light = mg.LightSource(Vec3(10,20,0))
    load = loader.Loader()
    cube = load.loadObj("cube.obj")
    cam = mg.Camera(Vec3(0, 0,-2), 0, -2.0)

    game = Main(MoteurGraphique, cam=cam,light=light)
    game.lunch()