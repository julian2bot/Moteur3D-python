import os
import lib_math as lb_math
import constante as const
from camera import Camera
from light_source import LightSource

width, height = os.get_terminal_size()
height -= 1


class MoteurGraphique:

    def __init__(self, width_cmd, height_cmd):
        self.width = width_cmd
        self.height = height_cmd
        self.pixel_buffer = [const.BACKGROUND] * (self.width * self.height)

    def draw(self: 'MoteurGraphique') -> None:
        print(''.join(self.pixel_buffer), end="")

    def clear(self: 'MoteurGraphique', char: str) -> None:
        for i in range(self.width * self.height):
            self.pixel_buffer[i] = char

    def put_pixel(self: 'MoteurGraphique', v: lb_math.Vec2, char: str) -> None:
        px = round(v.x)
        py = round(v.y)
        if (0 <= px <= self.width and 0 <= py <= self.height):
            self.pixel_buffer[py * self.width + px] = char

    def put_triangle(self: 'MoteurGraphique', tri: lb_math.Triangle3D,
                     char: str) -> None:

        def e(p: lb_math.Vec2, a: lb_math.Vec2, b: lb_math.Vec2) -> int:
            return (a.x - p.x) * (b.y - p.y) - (a.y - p.y) * (b.x - p.x)

        def est_dans_le_triangle(v1: lb_math.Vec2, v2: lb_math.Vec2,
                                 v3: lb_math.Vec2, p: lb_math.Vec2) -> bool:
            return e(v3, v1, p) > 0 and e(v2, v3, p) > 0 and e(
                v1, v2, p) > 0 or e(v3, v1, p) < 0 and e(v2, v3, p) < 0 and e(
                    v1, v2, p) < 0

        xmin = round(min(tri.v1.x, tri.v2.x, tri.v3.x))
        xmax = round(max(tri.v1.x, tri.v2.x, tri.v3.x) + 1)
        ymin = round(min(tri.v1.y, tri.v2.y, tri.v3.y))
        ymax = round(max(tri.v1.y, tri.v2.y, tri.v3.y) + 1)

        for y in range(ymin, ymax):
            if 0 <= y < self.height:
                for x in range(xmin, xmax):
                    if 0 <= x < self.width:
                        pos = lb_math.Vec2(x, y)

                        if est_dans_le_triangle(tri.v1, tri.v2, tri.v3, pos):
                            self.put_pixel(pos, char)

    def clip(self: 'MoteurGraphique', triangle: lb_math.Triangle3D,
             cam_pos: lb_math.Vec3,
             plane_normal: lb_math.Vec3) -> list[lb_math.Triangle3D]:

        def in_z(
            plane_normal: lb_math.Vec3, plane_point: lb_math.Vec3,
            tri: lb_math.Triangle3D
        ) -> tuple[list[lb_math.Vec3], list[lb_math.Vec3], bool]:

            out = []
            in_t = []

            vert1 = plane_normal.dot(plane_point - tri.v1)
            vert2 = plane_normal.dot(plane_point - tri.v2)
            vert3 = plane_normal.dot(plane_point - tri.v3)

            out.append(tri.v1) if vert1 > 0 else in_t.append(tri.v1)
            out.append(tri.v2) if vert2 > 0 else in_t.append(tri.v2)
            out.append(tri.v3) if vert3 > 0 else in_t.append(tri.v3)

            return out, in_t, vert1 * vert2 > 0

        z_near = cam_pos + 0.1 * plane_normal
        out, in_, is_inverted = in_z(plane_normal, z_near, triangle)

        if len(out) == 0:
            return [triangle]
        if len(out) == 3:
            return []
        if len(out) == 1:
            collision0 = plane_normal.line_plane_intersection(
                z_near, out[0], in_[0])
            collision1 = plane_normal.line_plane_intersection(
                z_near, out[0], in_[1])
            if is_inverted:
                return [
                    lb_math.Triangle3D(collision1, in_[1], collision0),
                    lb_math.Triangle3D(collision0, in_[1], in_[0])
                ]
            return [
                lb_math.Triangle3D(collision0, in_[0], collision1),
                lb_math.Triangle3D(collision1, in_[0], in_[1])
            ]

        if len(out) == 2:
            collision0 = plane_normal.line_plane_intersection(
                z_near, out[0], in_[0])
            collision1 = plane_normal.line_plane_intersection(
                z_near, out[1], in_[0])

            if is_inverted:
                return [
                    lb_math.Triangle3D(collision0, in_[0], collision1),
                ]
            return [
                lb_math.Triangle3D(collision0, collision1, in_[0]),
            ]

    def put_mesh(self: 'MoteurGraphique', mesh: list[lb_math.Triangle3D],
                 cam: Camera, light_source: LightSource) -> None:
        def distanceTriangleCam(triangle) -> float:
            position = (1/3) * (triangle.v1+triangle.v2+triangle.v3) - cam.position
            if position.lenght() <=0:
                print(position.lenght())
            return position.lenght()
        
        mesh.sort(key=distanceTriangleCam, reverse=True)
        look_at = cam.get_look_at_direction()

        for triangle in mesh:
            clipped_triangle_list = self.clip(triangle, cam.position, look_at)

            for clipped_triangle in clipped_triangle_list:
                line1 = clipped_triangle.v2 - clipped_triangle.v1
                line2 = clipped_triangle.v3 - clipped_triangle.v1
                surface_normal = line1.cross_prod(line2)

                if surface_normal.dot(clipped_triangle.v1 - cam.position) < 0:
                    light_str: str = light_source.diffuse_light(
                        surface_normal, clipped_triangle.v1)
                    self.put_triangle(
                        clipped_triangle.translate(
                            -1 * cam.position).rotation_y(cam.yaw).rotation_x(
                                cam.pitch).projection(
                                    cam.focal_lenth).to_screen(), light_str)
