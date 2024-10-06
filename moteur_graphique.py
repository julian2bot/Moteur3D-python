import os
from lib_math import * 
#CONSTANTE
BACKGROUND = ' '

width, height = os.get_terminal_size()

height -=1
pixelBuffer  = [BACKGROUND] * (width * height) 

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

    xmin = round(min(tri.p1.x, tri.p2.x, tri.p3.x))
    xmax = round(max(tri.p1.x, tri.p2.x, tri.p3.x)+1)
    ymin = round(min(tri.p1.y, tri.p2.y, tri.p3.y))
    ymax = round(max(tri.p1.y, tri.p2.y, tri.p3.y)+1)

    for y in range(ymin,ymax):
        if 0<=y<height:
            for x in range(xmin,xmax):
                if 0<=x<width:
                    pos = Vec2(x,y)

                    if(est_dans_le_triangle(tri.p1, tri.p2, tri.p3, pos)):
                        putPixel(pos,char)



# putPixel(Vec2(10,10), '#')
# tri = Triangle(
#     Vec2(10,10),
#     Vec2(40,10),
#     Vec2(40,50)
# )
# tri2 = Triangle(
#         Vec2(10,10),
#         Vec2(80,15),
#         Vec2(40,30)
#     )
# tri = Triangle(
#     Vec2(10,10),
#     Vec2(80,15),
#     Vec2(40,30)
# )
tri = Triangle(
    Vec2(24,0),
    Vec2(25,15),
    Vec2(1,20)
)

t = 0

while True:
    t+=0.01
    clear(BACKGROUND)
    
    tri.rotate(0.001)

    putTriangle(tri, "@")
    draw()

input()







