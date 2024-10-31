"""
    Librairie de calculs de vecteur 2d, 3d et triangle 2d ainsi que 3D
"""
import math
import moteur_graphique as mg
from constante import RADIO_PIXEL


class Vec2:
    """
        Vecteur en 2 dimensions
    """

    def __init__(self: 'Vec2', x: int, y: int) -> None:
        """
            Coordonnées x et y du vecteur en 2 dimensions


        Args:
            x (int): Coordonnées en x 
            y (int): Coordonnées en y 
        """
        self.x = x
        self.y = y

    def __mul__(self: 'Vec2', c: int) -> 'Vec2':
        """
            Multiplication d'un vecteur 2
            Calcul de x * c et y * c puis renvoyer un vecteur 2

        Args:
            c (int): Valeur par lequel multiplier notre vecteur

        Returns:
            Vec2: Vecteur multiplier par c
        """
        return Vec2(self.x * c, self.y * c)

    def __truediv__(self: 'Vec2', c: int) -> 'Vec2':
        """
            Division d'un vecteur 2
            Calcul de x / c et y / c puis renvoyer un vecteur 2

        Args:
            c (int): Valeur par lequel diviser notre vecteur

        Returns:
            Vec2: Vecteur diviser par c
        """
        return Vec2(self.x / c, self.y / c)

    def __add__(self: 'Vec2', v: 'Vec2') -> 'Vec2':
        """
            Addition d'un vecteur par un autre
            Calcul de x + x pour chaque vecteur et y + y pour chaque vecteur 

        Args:
            self (Vec2): Notre vecteur 2
            v (Vec2): Vecteur 2 à additionner

        Returns:
            Vec2: Resultat vecteur 2 
        """
        return Vec2(self.x + v.x, self.y + v.y)

    # pour permettre un calcul de deux vecteurs peu importe le sens
    # A = Vec2
    # B = Vec2
    # exemple d'opération  A + B ou B + A
    __radd__ = __add__
    __rmul__ = __mul__

    def to_screen(self: 'Vec2') -> 'Vec2':
        """ 
            Convertir les coordonnées normaliser au coordonne a la taille de l'écran
        
        exemple:
                        1,1
            +----------+
            |          |
            |    p     |
            |          |
            |          |
            +----------+
        -1,-1


                        800, 800
            +----------+
            |          |
            |    p     |
            |          |
            |          |
            +----------+
        0,0

        La formule pour faire ça:
            
            1. On additionne 1 pour plus avoir de nombre négatif
            
            Puis on aura donc 
                            2,2
                +----------+
                |          |
                |          |
                |          |
                |          |
                +----------+
            0,0
            
            2. Pour renormaliser ça, on divise par deux.

                            1,1
                +----------+
                |          |
                |          |
                |          |
                |          |
                +----------+
            0,0
            
            3. Puis on a donc des coordonnées entre 0 et 1 et avec cela, on multiplie par 
                la taille de l'écran

                            800, 800
                +----------+
                |          |
                |          |
                |          |
                |          |
                +----------+
            0,0

        Args:
            self (Vec2): Vecteur à normaliser

        Returns:
            Vec2: Vecteur normaliser
        """
        return Vec2(
            (RADIO_PIXEL * mg.height / mg.width * self.x + 1) * mg.width / 2,
            (-self.y + 1) * mg.height / 2)


class Vec3:
    """
        Vecteur en 3 dimensions
    """

    def __init__(self: 'Vec3', x: int, y: int, z: int) -> None:
        """
            Coordonnées x, y et z du vecteur en 3 dimensions

        Args:
            x (int): Coordonnées en x 
            y (int): Coordonnées en y 
            z (int): Coordonnées en z 
        """
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self: 'Vec3', c: int) -> 'Vec3':
        """
            Multiplication d'un vecteur 3
            Calcul de 
                      x * c 
                      y * c  
                      z * c
            Puis renvoyer un vecteur 3

        Args:
            c (int): Valeur par lequel multiplier notre vecteur

        Returns:
            Vec3: Vecteur multiplier par c
        """
        return Vec3(self.x * c, self.y * c, self.z * c)

    def __truediv__(self: 'Vec3', c: int) -> 'Vec3':
        """
            Division d'un vecteur 3
            Calcul de 
                      x / c 
                      y / c  
                      z / c
            Puis renvoyer un vecteur 3

        Args:
            c (int): Valeur par lequel diviser notre vecteur

        Returns:
            Vec3: Vecteur diviser par c
        """
        return Vec3(self.x / c, self.y / c, self.z / c)

    def __add__(self: 'Vec3', v: 'Vec3') -> 'Vec3':
        """
            Addition d'un vecteur par un autre
            Calcul de x + x pour chaque vecteur 
                      y + y pour chaque vecteur 
                      z + z pour chaque vecteur 

        Args:
            self (Vec3): Notre vecteur 3
            v (Vec3): Vecteur 3 à additionner

        Returns:
            Vec3: Resultat vecteur 3 
        """
        return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self: 'Vec3', v: 'Vec3') -> 'Vec3':
        """
            Soustraction d'un vecteur par un autre
            Calcul de x - x pour chaque vecteur 
                      y - y pour chaque vecteur 
                      z - z pour chaque vecteur 

        Args:
            self (Vec3): Notre vecteur 3
            v (Vec3): Vecteur 3 a soustraire

        Returns:
            Vec3: Resultat vecteur 3 
        """
        return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)

    # pour permettre un calcul de deux vecteurs peu importe le sens
    # A = Vec3
    # B = Vec3
    # exemple d'opération A + B ou B + A
    __radd__ = __add__
    __rmul__ = __mul__

    def projection(self, focal_lenth: int) -> 'Vec2':
        """
            Faire une projection en perspective de 2d en 3d 
            
            Calcul simplifié (sans matrice 4 dimensionnelle):
                Diviser les coordonnées par z et de multiplier par la distance focale
            
            Soit
                
                x, y ==> (f*(x/z) , f*(y/z))

                car:
           
           x' = f * x / z

           
        Camera               !                -
                             !           -            
                             !      -                °+--------------------+
                             ! -              °       1                    |    
                          -  !         °              1                    |   
            oO        -      l °                      1 x                  |       
        +------+  -    °     l x'                     1                    |       
        |      |/°___________l________________________1                    |           
        |      |\------------!                  Z     |                    |           
        +------+  -    f     !                        |                    |       
                      -      !                        |                    |       
                          -  !                        |                    |       
                             ! -                      |                    |       
                             !      -                 +--------------------+
                             !           -


        Args:
            focal_lenth (int): Distance focal

        Returns:
            Vec2: Vecteur 2 par rapport à la projection faite
        """
        return focal_lenth * Vec2(self.x, self.y) / self.z

    def rotation_x(self, pitch: int) -> 'Vec3':
        """
            Rotation en pitch (axe x) par rapport à la matrice de rotation 
                (ici juste l'utilisation final, pas des matrices)
                    z
                    |
                    |
                    |_______ y
                    / 
                |  / ∧
                 \- /
                 /
                x
        

        Args:
            pitch (int): Un angle pitch 

        Returns:
            Vec3: Vecteur3d avec les modifications (rotation en x) effectuée
        """
        y1 = math.cos(pitch) * self.y - math.sin(pitch) * self.z
        z1 = math.sin(pitch) * self.y + math.cos(pitch) * self.z
        return Vec3(self.x, y1, z1)

    def rotation_y(self, yaw: int) -> 'Vec3':
        """            
            Rotation en yaw (axe y) par rapport au calcul de la matrice de rotation 
                    z
                    |
                    |      \
                    |_______|___ y
                    /  ∧   /
                   /    \-/  
                  /
                 x

        Args:
            yaw (int): Un angle yaw

        Returns:
            Vec3: Vecteur3d avec les modifications (rotation en y) effectuée
        """
        x1 = math.cos(yaw) * self.x + math.sin(yaw) * self.z
        z1 = -math.sin(yaw) * self.x + math.cos(yaw) * self.z
        return Vec3(x1, self.y, z1)

    def dot(self: 'Vec3', v2: 'Vec3') -> float:
        """
            calculer le produit scalaire de deux vecteurs. 

        Args:
            self (Vec3): Vecteur 3D
            v2 (Vec3): Vecteur 3d

        Returns:
            float: Résultat du calcul du produit scalaire
        """
        # produit scalaire
        return self.x * v2.x + self.y * v2.y + self.z * v2.z

    def line_plane_intersection(self: 'Vec3', plane_point: 'Vec3', v1: 'Vec3',
                                v2: 'Vec3') -> 'Vec3':
        """
            Calculer l'intersection entre le plan et notre vecteur 

        
        Args:
            self (Vec3): Plan normal
            plane_point (Vec3): Vecteur 3d du plan
            v1 (Vec3): Le point de notre triangle
            v2 (Vec3): Le point de notre triangle

        Returns:
            Vec3: Intersection avec le plan
        """
        u = v2 - v1
        dotp = self.dot(u)
        if abs(dotp) < 1e-5:
            return (0, 0, 0)  # Pas d'intersection
        w = v1 - plane_point
        si = -self.dot(w) / dotp
        u = si * u
        return v1 + u

    def cross_prod(self: 'Vec3', v2: 'Vec3') -> 'Vec3':
        """
            Produit vectoriel 

        Args:
            self (Vec3): Vecteur 3d
            v2 (Vec3): Vecteur 3d

        Returns:
            Vec3: Vecteur 3d après le produit vectoriel des deux vecteurs 3d
        """
        # produit vectoriel
        return Vec3(self.y * v2.z - self.z * v2.y,
                    self.z * v2.x - self.x * v2.z,
                    self.x * v2.y - self.y * v2.x)

    def lenght(self: 'Vec3') -> float:
        """
            Distance via le théorème de pythagore

        Args:
            self (Vec3): Vecteur3d

        Returns:
            float: Résultat de la distance via le théorème de pythagore

        """
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self: 'Vec3') -> 'Vec3':
        """ 
            Normaliser un vecteur3d

        Args:
            self (Vec3): Vecteur 3d à normaliser

        Returns:
            Vec3: Vecteur 3d normaliser
        """
        norme = self.lenght()
        return Vec3(self.x / norme, self.y / norme, self.z / norme)


class Triangle2D:
    """
        Triangle en 2 dimension
    """

    def __init__(self: 'Triangle2D', v1: Vec2, v2: Vec2, v3: Vec2) -> None:
        """ 
            Création d'un triangle par rapport à 3 points (Vec2 => x,y)

        Args:
            self (Triangle2D): Triangle 2D
            v1 (Vec2): Point avec coordonées x et y 
            v2 (Vec2): Point avec coordonées x et y 
            v3 (Vec2): Point avec coordonées x et y 
        """
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def to_screen(self: 'Triangle2D') -> 'Triangle2D':
        """
            Convertir chaque sommet en coordonnée de l'écran

        Args:
            self (Triangle2D): Triangle 2d à convertir

        Returns:
            Triangle2D: Triangle 2d converti
        """
        return Triangle2D(self.v1.to_screen(), self.v2.to_screen(),
                          self.v3.to_screen())


class Triangle3D:
    """
        Triangle en 3 dimensions
    """

    def __init__(self: 'Triangle3D', v1: Vec3, v2: Vec3, v3: Vec3) -> None:
        """ 
            Création d'un triangle 3D par rapport à 3 points (Vec3 => x, y, z)

        Args:
            self (Triangle2D): Triangle 3D
            v1 (Vec3): Point avec coordonées x, y et z 
            v2 (Vec3): Point avec coordonées x, y et z 
            v3 (Vec3): Point avec coordonées x, y et z 
        """
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def projection(self: 'Triangle3D', focal_lenth: int) -> Triangle2D:
        """
            Projection de chaque point de notre triangle

        Args:
            self (Triangle3D): Triangle 3d
            focal_lenth (int): Distance focale

        Returns:
            Triangle2D: Triangle2D de la projection 
        """
        return Triangle2D(self.v1.projection(focal_lenth),
                          self.v2.projection(focal_lenth),
                          self.v3.projection(focal_lenth))

    def translate(self: 'Triangle3D', v: Vec3) -> 'Triangle3D':
        """ 
            Translation d'un triangle par rapport à un vecteur 3d

        Args:
            self (Triangle3D): Triangle 3D sur lequel appliquer la translation
            v (Vec3): Vecteur de translation

        Returns:
            Triangle3D: Nouveau triangle qui a bougé par rapport à la translation effectuée
        """
        return Triangle3D(self.v1 + v, self.v2 + v, self.v3 + v)

    def rotation_x(self: 'Triangle3D', pitch: int) -> 'Triangle3D':
        """
            Appliquer la rotation en x sur tous les points du Triangle 3d

        Args:
            self (Triangle3D): Triangle3d sur lequel appliquer la rotation
            pitch (int): Angle de pitch 

        Returns:
            Triangle3D: Triangle avec la rotation 
        """
        return Triangle3D(self.v1.rotation_x(pitch), self.v2.rotation_x(pitch),
                          self.v3.rotation_x(pitch))

    def rotation_y(self: 'Triangle3D', yaw: int) -> 'Triangle3D':
        """
            Appliquer la rotation en y sur tous les points du Triangle 3d

        Args:
            self (Triangle3D): Triangle3d sur lequel appliquer la rotation
            yaw (int): Angle de pitch 

        Returns:
            Triangle3D: Triangle avec la rotation 
        """
        return Triangle3D(self.v1.rotation_y(yaw), self.v2.rotation_y(yaw),
                          self.v3.rotation_y(yaw))
