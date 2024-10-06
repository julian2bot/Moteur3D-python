import moteur_graphique as mg
from lib_math import *
import constante as const

# tri = Triangle2D(Vec2(-0.5,-0.5),
#                Vec2( 0  , 0.5),
#                Vec2( 0.5,-0.5))

tri = Triangle3D(Vec3(-0.5,-0.5,1),
               Vec3( 0  , 0.5  ,1),
               Vec3( 0.5,-0.5  ,1))

t= 0
while True:
    mg.clear(const.BACKGROUND)
    t+=.001
    # mg.putTriangle(tri.translate(Vec3(0.3,0.5,0.5)).projection().toScreen(), "@")
    # mg.putTriangle(tri.projection().toScreen(), "@")
    # mg.putTriangle(tri.rotationX(t).translate(Vec3(0,0,2)).projection().toScreen(), "@")
    mg.putTriangle(tri.rotationX(t).rotationY(t).translate(Vec3(0,0,2)).projection().toScreen(), "@")
    
    mg.draw()

input()







