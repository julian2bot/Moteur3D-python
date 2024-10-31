"""
    Convertisseur .obj en triangle utilisable pour le moteur graphique
"""
from lib_math import Triangle3D, Vec3


class Loader:
    """
        Convertisseur de fichier .obj en mesh (Triangle 3d)
    """

    def __init__(self: 'Loader') -> None:
        pass

    def load_object(self: 'Loader', file_path: str) -> list[Triangle3D]:
        """
            Renvoie une liste de triangles par rapport au fichier d'un objet 3D 
                en .obj qu'on lui donne

            exemple:
            mtllib ./cube.mtl

            v -0.500000 -0.500000 -0.500000  ==>  indexé par 1
            v -0.500000 0.500000 -0.500000   ==>  indexé par 2
            v 0.500000 -0.500000 -0.500000   ==>  indexé par 3
            v 0.500000 0.500000 -0.500000    ==>  indexé par 4
            v 0.500000 -0.500000 0.500000    ==>  indexé par 5
            v 0.500000 0.500000 0.500000     ==>  indexé par 6
            v -0.500000 -0.500000 0.500000   ==>  indexé par 7
            v -0.500000 0.500000 0.500000    ==>  indexé par 8
            # 8 vertices

            o Cube
            usemtl default
            f 1 2 4 3
            f 3 4 6 5
            f 5 6 8 7
            f 7 8 2 1
            f 2 8 6 4
            f 7 1 3 5


            Le fichier cube.obj
            Nous avons les f (face) et les v (vertice)
                        
            Les faces sont des index pour les vecteurs exemples:

            f 1 2 4 3
                Qui signifie qu'il y a un triangle avec les index 1 2 4 et 4 3 1
            soit 
                Premier triangle = les trois premiers index ;
                Le second triangle est les deux dernier index suivie du premier.

                Et cela pour chaque face


                Configuration pour avoir cette forme de fichier :
                    Dans blender, cinema4d (ou autre),
                        Créer un objet => l'exporter => en obj
                            Mettre à l'échelle => objet de 200 cm par exemple mettre 
                                un scale a 200 (Pour après avoir un cube entre -0.5 et 0.5)
                            Désactiver les coordonnées Uvs (mettre à None)
                            Désactiver les normales (mettre à None)
                    Puis exporter en .obj²

        Args:
            self (Loader): Loader
            file_path (str): Fichier en .obj

        Returns:
            list[Triangle3D]: Liste des triangles crée par rapport à l'objet 3d
        """
        with open(file_path, "r", encoding='utf-8') as file:
            lines = [
                line.rstrip('\n').split(' ') for line in file.readlines()
                if line.rstrip('\n')
            ]

            vertices = []
            faces = []
            for line in lines:
                if line[0] == 'v':
                    vertex = list(map(float, line[1:]))
                    vertices.append(Vec3(vertex[0], vertex[1], vertex[2]))
                if line[0] == 'f':
                    faces.append(list(map(int, line[1:])))

            triangles = []
            for face in faces:
                if len(face) == 3:
                    triangles.append(
                        Triangle3D(vertices[face[0] - 1],
                                   vertices[face[1] - 1],
                                   vertices[face[2] - 1]))
                if len(face) == 4:
                    triangles.append(
                        Triangle3D(vertices[face[0] - 1],
                                   vertices[face[1] - 1],
                                   vertices[face[2] - 1]))
                    triangles.append(
                        Triangle3D(vertices[face[2] - 1],
                                   vertices[face[3] - 1],
                                   vertices[face[0] - 1]))
            return triangles
