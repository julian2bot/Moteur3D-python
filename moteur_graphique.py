import os
from lib_math import * 
import constante as const
width, height = os.get_terminal_size()

height -=1
pixelBuffer  = [const.BACKGROUND] * (width * height) 

def draw():
    print(''.join(pixelBuffer), end="")

def clear(char):
    for i in range(width * height):
        pixelBuffer[i] = char

def putPixel(V,char):
    px= round(V.x)
    py= round(V.y)
    if (0<= px <= width and 0<= py <= height):
        pixelBuffer[py*width+px] = char

def putTriangle(tri, char):
    def E(p,a,b) -> int:
        return (a.x - p.x)*(b.y - p.y)-(a.y - p.y)*(b.x - p.x)
    def est_dans_le_triangle(v1, v2, v3, p) -> bool:
        return E(v3,v1,p)>0 and E(v2,v3,p)>0 and E(v1,v2,p)>0 or E(v3,v1,p)<0 and E(v2,v3,p)<0 and E(v1,v2,p)<0 

    xmin = round(min(tri.v1.x, tri.v2.x, tri.v3.x))
    xmax = round(max(tri.v1.x, tri.v2.x, tri.v3.x)+1)
    ymin = round(min(tri.v1.y, tri.v2.y, tri.v3.y))
    ymax = round(max(tri.v1.y, tri.v2.y, tri.v3.y)+1)

    for y in range(ymin,ymax):
        if 0<=y<height:
            for x in range(xmin,xmax):
                if 0<=x<width:
                    pos = Vec2(x,y)

                    if(est_dans_le_triangle(tri.v1, tri.v2, tri.v3, pos)):
                        putPixel(pos,char)

