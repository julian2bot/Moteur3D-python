# import openstl
# import numpy as np

# # Define an array of triangles
# # Following the STL standard, each triangle is defined with : normal, v0, v1, v2
# quad = np.array([
#     # normal,          vertices 0,      vertices 1,      vertices 2
#     [[0.0, 0.0, 1.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]], # Triangle 1
#     [[0.0, 0.0, 1.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]], # Triangle 2
# ])

# # Write
# # success = openstl.write("rectangle.stl", quad, openstl.format.binary) # Or openstl.format.ascii (slower but human readable)

# # Read
# quad = openstl.read("rectangle.stl")
# print(quad)

import meshio

mesh = meshio.read("rectangle.stl")  # or .off, .vtk, .ply, ...
# mesh.points, mesh.cells, ...
# print(mesh.points)
# print(mesh.points)

triangles_points = []

# Accéder aux triangles à partir de mesh.cells[0].data
for triangle in mesh.cells[0].data:
    # Récupérer les coordonnées des trois points qui forment le triangle
    p1 = mesh.points[triangle[0]]  # Premier point du triangle
    p2 = mesh.points[triangle[1]]  # Deuxième point du triangle
    p3 = mesh.points[triangle[2]]  # Troisième point du triangle

    print('p1', p1)
    print('p2', p2)
    print('p3', p3)

    # # Ajouter ces trois points à la liste triangles_points
    # triangles_points.append([p1, p2, p3])

# Afficher les triangles avec leurs points
# for triangle in triangles_points:
#     print(f"Triangle formed by points: {triangle}")

# print(triangles_points[0][0])
