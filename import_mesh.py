# fichier pour tester l'import de STL avec mishio (pas convaincu lol)
import meshio
import numpy as np
import constante as const
from lib_math import Triangle3D, Vec3

# mesh.points, mesh.cells, ...


class StlToMesh:

    def __init__(self, path):
        self.path = path

    def read_stl(self):

        mesh = meshio.read(self.path)  # or .off, .vtk, .ply, ...
        points = np.array(mesh.points)
        min_val = points.min(axis=0)
        max_val = points.max(axis=0)

        def normalize_point(point, min_vals, max_vals):
            return 2 * ((point - min_vals) / (max_vals - min_vals)) - 1

        normalized_points = np.array([
            normalize_point(point, min_val, max_val) for point in mesh.points
        ])

        forme = []
        for triangle in mesh.cells[0].data:

            p1 = normalized_points[triangle[0]]
            p2 = normalized_points[triangle[1]]
            p3 = normalized_points[triangle[2]]

            forme.append(
                Triangle3D(Vec3(p1[const.X], p1[const.Y], p1[const.Z]),
                           Vec3(p2[const.X], p2[const.Y], p2[const.Z]),
                           Vec3(p3[const.X], p3[const.Y], p3[const.Z])))
