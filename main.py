import time
from pynput.mouse import Listener
import moteur_graphique as mg
from lib_math import Vec3, Triangle3D
import constante as const
import loader


class Main:

    def __init__(self: 'Main', graphics_engine: mg.MoteurGraphique,
                 triangle_list: list[Triangle3D], camera: mg.Camera,
                 light_source: mg.LightSource) -> None:
        self.moteur_graphique = graphics_engine
        self.cam = camera
        self.triangles = triangle_list
        self.dernier = 0
        self.light = light_source
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
            self.cam.inputs(dt)
            # souris a faire
            self.cam.prev_mouse_x, self.cam.prev_mouse_y = self.cam.cam_move(
                self.cam.prev_mouse_x, self.cam.prev_mouse_y,
                self.cam.mouse_dx, self.cam.mouse_dy, dt)
            self.moteur_graphique.put_mesh(self.triangles, self.cam,
                                           self.light)
            self.moteur_graphique.draw()


if __name__ == "__main__":

    moteur_graphique = mg.MoteurGraphique(mg.width, mg.height)

    light = mg.LightSource(Vec3(10, 20, 0))
    load = loader.Loader()
    cube = load.load_object("cube.obj")
    cam = mg.Camera(Vec3(0, 0, -2), 0, -2.0)

    game = Main(moteur_graphique,
                triangle_list=cube,
                camera=cam,
                light_source=light)
    game.lunch()
