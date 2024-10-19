
import constante as const
from moteur_graphique import Triangle3D, Vec3 
import numpy as np
import meshio


mesh = meshio.read("rectangle.stl")  # or .off, .vtk, .ply, ...
# mesh.points, mesh.cells, ...


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

