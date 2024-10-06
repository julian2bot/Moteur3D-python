import math 


class Vec2:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    def rotate(self, angle, center):
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)

        x_translated = self.x - center.x
        y_translated = self.y - center.y

        x_rotated = x_translated * cos_theta - y_translated * sin_theta
        y_rotated = x_translated * sin_theta + y_translated * cos_theta

        self.x = x_rotated + center.x
        self.y = y_rotated + center.y



class Triangle:
    def __init__(self,p1,p2,p3) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    
    def center(self):
        cx = (self.p1.x + self.p2.x + self.p3.x) / 3
        cy = (self.p1.y + self.p2.y + self.p3.y) / 3
        return Vec2(cx, cy)

    def rotate(self, angle):
        center = self.center()
        self.p1.rotate(angle, center)
        self.p2.rotate(angle, center)
        self.p3.rotate(angle, center)
