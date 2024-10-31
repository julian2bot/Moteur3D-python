"""
    Une camera pour le moteur graphique.
"""
import sys
import math
import keyboard
from lib_math import Vec3
import constante as const


class Camera:
    """
        Le point de vue qu'on aura, la camera   
    """

    def __init__(self: 'Camera',
                 position: Vec3,
                 pitch: float,
                 yaw: float,
                 focal_lenth: int = 1) -> None:
        """
            Création de la camera par rapport à sa position, angle et distance focale initiale

        Args:
            self (Camera): camera
            position (Vec3): Position x, y et z
            pitch (float): Angle pitch
            yaw (float): Angle yaw
            focal_lenth (int, optional): Distance focale. Defaults to 1.
        """
        self.position = position
        self.pitch = pitch
        self.yaw = yaw
        self.focal_lenth = focal_lenth
        self.mouse_dx = 0
        self.mouse_dy = 0
        self.prev_mouse_x = 0
        self.prev_mouse_y = 0

        # a revoir
        self.jump_max = 2
        self.jump = 0.2
        self.is_jumping = False
        self.has_jumped = False

    def get_look_at_direction(self: 'Camera') -> Vec3:
        """
            Renvoie un vecteur de là où la camera regarde avec l'utilisation 
                des coordonnées sphériques  
                (juste la formule pour passé 
                    de coordonnées sphérique en coordonnées cartésiennes)

        Args:
            self (Camera): Camera

        Returns:
            Vec3: Vecteur en face de la camera (vecteur de là où la camera regarde)
        """
        return Vec3(-math.sin(self.yaw) * math.cos(self.pitch),
                    math.sin(self.pitch),
                    math.cos(self.yaw) * math.cos(self.pitch))

    def get_forward_direction(self: 'Camera') -> Vec3:
        """
            Renvoie le vecteur qui est en face de la camera, selon l'orientation de la camera
                via la trigonométrie et module math
        Args:
            self (Camera): Camera

        Returns:
            Vec3: Vecteur en face de la camera
        """
        return Vec3(-math.sin(self.yaw), 0, math.cos(self.yaw))

    def get_right_direction(self: 'Camera') -> Vec3:
        """
            Renvoie le vecteur qui est à droite de la camera, selon l'orientation de la 
                camera via la trigonométrie et module math

        Args:
            self (Camera): Camera

        Returns:
            Vec3: Vecteur à droite de la camera
        """
        return Vec3(math.cos(self.yaw), 0, math.sin(self.yaw))

    def inputs(self: 'Camera', dt: float) -> None:
        """
            Gérer la position, angles de la camera par rapport 
                aux touches du clavier gestion des touches via le module keyboard

            Les touches :

            z ==> avancer
            q ==> aller à gauche
            s ==> reculer 
            d ==> aller à droite

            Flèche haut   ==> orientation sur l'axe x, regarder en haut  
            Flèche bas    ==> orientation sur l'axe x, regarder en bas
            Flèche gauche ==> orientation sur l'axe y, regarder à gauche
            Flèche droite ==> orientation sur l'axe y, regarder à droite

            Espace ==> monter   
            Shift  ==> descendre

            c  ==> quitter le programme (car les touches sont captées par python 
                et plus par le cmd donc sans ça nous ne pouvons pas quitter)

        Args:
            self (Camera): Camera
            dt (float): Un temps
        """

        if keyboard.is_pressed("down arrow"):
            if self.pitch > -const.PI_SUR_DEUX:
                self.pitch -= const.DEFAULT_DEPLACEMENT * dt
        if keyboard.is_pressed("up arrow"):
            if self.pitch < const.PI_SUR_DEUX:
                self.pitch += const.DEFAULT_DEPLACEMENT * dt

        if keyboard.is_pressed("left arrow"):
            self.yaw += const.DEFAULT_DEPLACEMENT * dt
        if keyboard.is_pressed("right arrow"):
            self.yaw -= const.DEFAULT_DEPLACEMENT * dt

        if keyboard.is_pressed("z"):
            self.position += self.get_forward_direction(
            ) * const.DEFAULT_DEPLACEMENT * dt
        if keyboard.is_pressed("s"):
            self.position += -1 * self.get_forward_direction(
            ) * const.DEFAULT_DEPLACEMENT * dt

        if keyboard.is_pressed("d"):
            self.position += self.get_right_direction(
            ) * const.DEFAULT_DEPLACEMENT * dt
        if keyboard.is_pressed("q"):
            self.position += -1 * self.get_right_direction(
            ) * const.DEFAULT_DEPLACEMENT * dt

        # a revoir
        if keyboard.is_pressed("space") \
                and self.position.y < self.jump and self.has_jumped == False:
            if self.is_jumping == False:
                self.jump = self.position.y + self.jump_max
                self.is_jumping = True
            self.position.y += const.DEFAULT_JUMP * dt
        else:
            self.is_jumping = False
            self.has_jumped = True

        if keyboard.is_pressed("shift") and self.position.y >= 0.2:
            self.position.y -= const.DEFAULT_GRAVITE * dt

        # if keyboard.is_pressed("a"):
        #     self.focalLenth += .1 * dt
        # if keyboard.is_pressed("e"):
        #     self.focalLenth -= .1 * dt

        # gravité
        if keyboard.is_pressed("c"):
            sys.exit()

    def cam_move(self: 'Camera', prev_mouse_x: int, prev_mouse_y: int,
                 mouse_dx: int, mouse_dy: int, dt: float) -> tuple[int, int]:
        """ 
            Mouvement de la camera par rapport à la souris

        Args:
            self (Camera): Camera
            prev_mouse_x (int): Pos x de la souris avant
            prev_mouse_y (int): Pos y de la souris avant
            mouse_dx (int): Pos x de la souris maintenant 
            mouse_dy (int): Pos y de la souris maintenant 
            dt (float): Interval de temps

        Returns:
            tuple[int, int]: Envoie les positions actuelles de la souris
        """
        delta_x = mouse_dx - prev_mouse_x
        delta_y = mouse_dy - prev_mouse_y
        self.yaw -= delta_x * const.DEFAULT_DEPLACEMENT / 2 * dt
        self.pitch -= delta_y * const.DEFAULT_DEPLACEMENT / 3 * dt
        prev_mouse_x = mouse_dx
        prev_mouse_y = mouse_dy
        return prev_mouse_x, prev_mouse_y

    def on_move(self: 'Camera', x: int, y: int) -> None:
        """ 
            Position de la souris sur l'écran selon pos x et y

        Args:
            self (Camera): Camera
            x (int): Position x de la souris 
            y (int): Position y de la souris 
        """
        self.mouse_dx = x  # pos x de la souris
        self.mouse_dy = y  # pos y de la souris
        # return self.mouse_dx, self.mouse_dy

    def __str__(self: 'Camera'):
        """ Renvoie un texte avec la position x y z et l'angle yaw et pitch de la camera.

        Returns:
            str: Texte position + angle camera
        """
        return "" + str(self.position.x) + " " + str(
            self.position.y) + " " + str(self.position.z) + " " + str(
                self.yaw) + " " + str(self.pitch)
