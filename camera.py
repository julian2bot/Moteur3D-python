import sys
import math
import keyboard
from lib_math import Vec3
import constante as const


class Camera:

    def __init__(self: 'Camera',
                 position: Vec3,
                 pitch: float,
                 yaw: float,
                 focal_lenth: int = 1) -> None:
        self.position = position
        self.pitch = pitch
        self.yaw = yaw
        self.focal_lenth = focal_lenth
        self.mouse_dx = 0
        self.mouse_dy = 0
        self.prev_mouse_x = 0
        self.prev_mouse_y = 0

    def get_look_at_direction(self: 'Camera') -> Vec3:
        return Vec3(-math.sin(self.yaw) * math.cos(self.pitch),
                    math.sin(self.pitch),
                    math.cos(self.yaw) * math.cos(self.pitch))

    def get_forward_direction(self: 'Camera') -> Vec3:
        return Vec3(-math.sin(self.yaw), 0, math.cos(self.yaw))

    def get_right_direction(self: 'Camera') -> Vec3:
        return Vec3(math.cos(self.yaw), 0, math.sin(self.yaw))

    def inputs(self: 'Camera', dt: float) -> None:
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

        if keyboard.is_pressed("space"):
            self.position.y += const.DEFAULT_DEPLACEMENT * dt
        if keyboard.is_pressed("shift"):
            self.position.y -= const.DEFAULT_DEPLACEMENT * dt

        # if keyboard.is_pressed("a"):
        #     self.focalLenth += .1 * dt
        # if keyboard.is_pressed("e"):
        #     self.focalLenth -= .1 * dt

        if keyboard.is_pressed("c"):
            sys.exit()

    def cam_move(self: 'Camera', prev_mouse_x: int, prev_mouse_y: int,
                 mouse_dx: int, mouse_dy: int, dt: float) -> tuple[int, int]:
        delta_x = mouse_dx - prev_mouse_x
        delta_y = mouse_dy - prev_mouse_y
        self.yaw -= delta_x * const.DEFAULT_DEPLACEMENT / 2 * dt
        self.pitch -= delta_y * const.DEFAULT_DEPLACEMENT / 3 * dt
        prev_mouse_x = mouse_dx
        prev_mouse_y = mouse_dy
        return prev_mouse_x, prev_mouse_y

    def on_move(self: 'Camera', x: int, y: int) -> None:

        self.mouse_dx = x  # pos x de la souris
        self.mouse_dy = y  # pos y de la souris
        # return self.mouse_dx, self.mouse_dy
