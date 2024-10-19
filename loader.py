from lib_math import *


class Loader:
    def __init__(self):
        pass        
    def loadObj(self,filePath):
        with open(filePath, "r") as file:
            lines = [line.rstrip('\n').split(' ') for line in file.readlines() if line.rstrip('\n') ]

            vertices= []
            faces = []
            for line in lines:
                if line[0]== 'v':
                    vertex = list(map(float, line[1:]))
                    vertices.append(Vec3(vertex[0],vertex[1],vertex[2]))        
                if line[0]== 'f':
                    faces.append(list(map(int,line[1:])))

            triangles = []
            for face in faces:
                if len(face) == 3:
                    triangles.append(Triangle3D(vertices[face[0]-1],vertices[face[1]-1],vertices[face[2]-1]))
                if len(face) == 4:
                    triangles.append(Triangle3D(vertices[face[0]-1],vertices[face[1]-1],vertices[face[2]-1]))
                    triangles.append(Triangle3D(vertices[face[2]-1],vertices[face[3]-1],vertices[face[0]-1]))
            return triangles

