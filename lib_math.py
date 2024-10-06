import moteur_graphique as mg
import math
class Vec2:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

    def __mul__(self,c):
        return Vec2(self.x*c,self.y*c)
    
    def __truediv__(self,c):
        return Vec2(self.x/c,self.y/c)
    
    def __add__(self,v):
        return Vec2(self.x+v.x,self.y+v.y)
    
    __radd__ = __add__
    __rmul__ = __mul__

    def toScreen(self):
        return Vec2(((29/13)*mg.height/mg.width*self.x+1)*mg.width/2,
                    (-self.y+1)*mg.height/2)
    
class Vec3:
    def __init__(self,x,y,z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self,c):
        return Vec3(self.x*c,self.y*c,self.z*c)
    
    def __truediv__(self,c):
        return Vec3(self.x/c,self.y/c,self.z/c)
    
    def __add__(self,v):
        return Vec3(self.x+v.x,self.y+v.y,self.z+v.z)
    
    __radd__ = __add__
    __rmul__ = __mul__

    def projection(self):
        return Vec2(self.x, self.y) / self.z

    def rotationX(self,pitch):
        y1= math.cos(pitch) * self.y - math.sin(pitch) * self.z
        z1= math.sin(pitch) * self.y + math.cos(pitch) * self.z
        return Vec3(self.x, y1, z1)

    def rotationY(self,yaw):
        x1=  math.cos(yaw) * self.x - math.sin(yaw) * self.z
        z1= -math.sin(yaw) * self.x + math.cos(yaw) * self.z
        return Vec3(x1, self.y, z1)

class Triangle2D:
    def __init__(self,v1,v2,v3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    
    def toScreen(self):
        return Triangle2D(
            self.v1.toScreen(),
            self.v2.toScreen(),
            self.v3.toScreen()
        )
        

class Triangle3D:
    def __init__(self,v1,v2,v3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def projection(self):
        return Triangle2D(self.v1.projection(),self.v2.projection(),self.v3.projection())
    
    def translate(self, v:Vec3):
        return Triangle3D(self.v1+v,self.v2+v,self.v3+v)

    def rotationX(self, pitch):
        return Triangle3D(self.v1.rotationX(pitch),self.v2.rotationX(pitch),self.v3.rotationX(pitch))

    def rotationY(self, yaw):
        return Triangle3D(self.v1.rotationY(yaw),self.v2.rotationY(yaw),self.v3.rotationY(yaw))


