"""
    Fichier Principal du moteur graphique
"""
import time
from pynput.mouse import Listener
import moteur_graphique as mg
from lib_math import Vec3, Triangle3D
import constante as const
import loader


class Main:
    """
        Classe principale pour exécution du moteur graphique dans le terminal
    """

    def __init__(self: 'Main', graphics_engine: mg.MoteurGraphique,
                 triangle_list: list[Triangle3D], camera: mg.Camera,
                 light_source: mg.LightSource, acceleration: float) -> None:
        """
            Initialisation du main

        Args:
            self (Main): Main
            graphics_engine (mg.MoteurGraphique): Moteur graphique
            triangle_list (list[Triangle3D]): Liste des triangles à afficher
            camera (mg.Camera): Camera qu'on utilise
            light_source (mg.LightSource): Source de lumière qu'on utilise
            acceleration (float): Gravité
        """
        self.moteur_graphique = graphics_engine
        self.cam = camera
        self.triangles = triangle_list
        self.dernier = 0
        self.light = light_source

        # Souris à faire
        self.listener = Listener(on_move=self.cam.on_move)

        self.mouse_dx = 0
        self.mouse_dy = 0
        self.prev_mouse_x, self.prev_mouse_y = self.mouse_dx, self.mouse_dy
        self.acceleration = acceleration

    def lunch(self: 'Main') -> None:
        """
            Lancement du moteur graphique

        Args:
            self (Main): Main
        """
        # Souris à faire

        # listener = Listener(on_move=self.cam.on_move)
        # listener.start()
        self.listener.start()
        while True:
            self.acceleration
            temps_actuelle = time.time()
            dt = (temps_actuelle - self.dernier) * 100
            # time.sleep(0.01)
            self.dernier = temps_actuelle

            # if self.cam.position.y < self.cam.jump and self.cam.has_jumped == False:

            #     self.cam.is_jumping = True
            # else:
            #     self.cam.is_jumping = False
            #     self.cam.has_jumped = True

            # a revoir
            if self.cam.has_jumped == True and self.cam.position.y >= 0.2:
                self.cam.position.y -= const.DEFAULT_DEPLACEMENT / 4
            else:
                self.cam.has_jumped = False

            # if self.cam.is_jumping == False and self.cam.position.y >= 0.2 :
            #       # and not keyboard.is_pressed("space"):
            #     self.cam.position.y -= const.DEFAULT_DEPLACEMENT/4

            # input()
            self.moteur_graphique.clear(const.BACKGROUND)
            self.cam.inputs(dt)

            # Lumière qui bouge
            self.light.move(dt)

            # Souris à faire
            self.cam.prev_mouse_x, self.cam.prev_mouse_y = self.cam.cam_move(
                self.cam.prev_mouse_x, self.cam.prev_mouse_y,
                self.cam.mouse_dx, self.cam.mouse_dy, dt)
            self.moteur_graphique.put_mesh(self.triangles, self.cam,
                                           self.light)
            self.moteur_graphique.draw()


if __name__ == "__main__":

    # créer le moteur graphique
    moteur_graphique = mg.MoteurGraphique(mg.width, mg.height)

    # créer la source de lumière à des coordonnées données
    light = mg.LightSource(Vec3(10, 20, 0))

    # créer notre liste de triangles grâce au fichier cube.obj
    load = loader.Loader()
    cube = load.load_object("cube.obj")

    # créer notre camera à une position et orientation donnée
    #   (ici mis à une valeur qui semble bien pour visualiser le cube directement)
    cam = mg.Camera(
        Vec3(0.8734519486135826, 1.1599074363708497, -1.0721290930719833),
        -0.8587246735890687, -5.735267162322998)

    # créer notre main
    game = Main(moteur_graphique,
                triangle_list=cube,
                camera=cam,
                light_source=light,
                acceleration=-(const.DEFAULT_DEPLACEMENT / 2))

    # lancer le moteur graphique avec tout les paramètres données !
    game.lunch()
