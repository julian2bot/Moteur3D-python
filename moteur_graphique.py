"""
    Classe MoteurGraphique
"""
import os
import lib_math as lb_math
import constante as const
from camera import Camera
from light_source import LightSource

# Taille de la console
width, height = os.get_terminal_size()
# La dernière ligne jamais utilisée
height -= 1


class MoteurGraphique:
    """
        Classe du moteur graphique avec toutes les fonctions qui construit et affiche nos formes
    """

    def __init__(self, width_cmd, height_cmd):
        """
            création du moteur graphique avec ça taille
        Args:
            width_cmd (_type_): largeur du terminal
            height_cmd (_type_): hauteur du terminal
        """
        self.width = width_cmd
        self.height = height_cmd
        # liste qui sera affiché avec tout les pixels de l'ecran (dimension 1)
        self.pixel_buffer = [const.BACKGROUND] * (self.width * self.height)

    def draw(self: 'MoteurGraphique') -> None:
        """
            Afficher la liste dans le terminal

        Args:
            self (MoteurGraphique): le moteur graphique
        """
        print(''.join(self.pixel_buffer), end="")

    def clear(self: 'MoteurGraphique', char: str) -> None:
        """
            reset la liste qui est affiché avec des caractères vides

        Args:
            self (MoteurGraphique): moteur graphique
            char (str): Caractère à mettre pour chaque index de ma liste 
                (par défaut, le caractère est vide)
        """
        for i in range(self.width * self.height):
            self.pixel_buffer[i] = char

    def put_pixel(self: 'MoteurGraphique', v: lb_math.Vec2, char: str) -> None:
        """
            Placer un caractère a une coordonnas 

        Args:
            self (MoteurGraphique): Moteur graphique
            v (lb_math.Vec2): Vec2 classe avec deux points, x et y
            char (str): Caracetere à poser 
        """
        px = round(v.x)
        py = round(v.y)
        if (0 <= px <= self.width and 0 <= py <= self.height):
            self.pixel_buffer[py * self.width + px] = char

    def put_triangle(self: 'MoteurGraphique', tri: lb_math.Triangle3D,
                     char: str) -> None:
        """ 
            Poser un triangle par rapport à ses points est le rempli du caractère donné
        
        Args:
            self (MoteurGraphique): Moteur graphique
            tri (lb_math.Triangle3D): Un triangle 3D à poser
            char (str): Le caractère avec lequel sera affiché le triangle
        """

        def e(p: lb_math.Vec2, a: lb_math.Vec2, b: lb_math.Vec2) -> int:
            """Savoir de quel côté est un point par rapport à une droite
                
                Explication détaillée:
                    On calcul l'air du parallélogramme qui relie p aux deux points a et b
                
                    Si l'air est positif > 0 alors le point est a droite sinon si l'air 
                    Et négatif < 0 le point sera a gauche
                    Et ce sera inversé si les deux sommets sont inversés
                        
                        a
                        |    
                        |    p+
                        |    
 
                        b

                        ou
                        
                        a
                        |    
               p-       |    
                        |    
                        b

------------------------OU------------------------

                        b
                        |    
                        |    p-
                        |    
 
                        a

                        ou
                        
                        b
                        |    
               p+       |    
                        |    
                        a

                Ce qui est calculé est le produit vectoriel. (det)
                Ça renvoie un vecteur normal eagle a l'air du parallélogramme. 
                Exemple avec | qui est le vecteur normal

            + air positif
           /|\ 
            |            -
            |          -
            |        -
            |      -            
            |    -            
            |  -            
            |-
             -------------------------
            |
            |
            |
            |
            |
            |
           \|/ 
            - air negatif

            Donc le calcul est 

                /                  \
            det | (V2x-Px) (V1x-Px) |
                | (V2y-Py) (V1y-Py) | 
                \                  /
            
            Soit:
            
                (V2x-Px)(V1y-Py) - (V2y-Py)(V1x-Px)
            
                

            Si (V2x-Px)(V1y-Py) - (V2y-Py)(V1x-Px) > 0


                        v2
                        |    
               p        |    
                        |    
                        v1
            Si (V2x-Px)(V1y-Py) - (V2y-Py)(V1x-Px) < 0


                        v2
                        |    
                        |    p
                        |    
                        v1

            Args:
                p (lb_math.Vec2): Point a tester 
                a (lb_math.Vec2): Point qui est sur notre droite
                b (lb_math.Vec2): Point qui est sur notre droite

            Returns:
                int: Valeur calcul de l'air
            """
            return (a.x - p.x) * (b.y - p.y) - (a.y - p.y) * (b.x - p.x)

        def est_dans_le_triangle(v1: lb_math.Vec2, v2: lb_math.Vec2,
                                 v3: lb_math.Vec2, p: lb_math.Vec2) -> bool:
            """
                Regarde si un point p est dans un triangle, renvoie True si oui false sinon

                    V3
                  /   \
                 /     \ 
                /       \  
               /     p   \
              /           \
             /             \
            V1--------------V2

            si: 
                e(v3, v1, p) > 0 
                e(v1, v2, p) > 0 
                e(v2, v3, p) > 0 

                alors p est dans le triangle
                
            Si une est fausse p est en dehors du triangle:
                
                    V3
                  /   \
                 /     \ 
                /       \  
          p    /         \
              /           \
             /             \
            V1--------------V2

            si: 
                e(v3, v1, p) < 0 
                e(v1, v2, p) > 0 
                e(v2, v3, p) > 0 

            Mais si selon l'orientation un test bon n'est plus valable car 
                
                    V2
                  /   \
                 /     \ 
                /       \  
               /     p   \
              /           \
             /             \
            V1--------------V3

            V2 et V3 sont inversées et le test est sensé entre correcte, mais ne 
            l'ai pas donc on peut tester en plus 

            si: 
                e(v3, v1, p) < 0 
                e(v1, v2, p) < 0 
                e(v2, v3, p) < 0 

            Avec ça comme le point ne peux pas être à l'extérieur de chaque 
                coté du triangle, on sait qu'il sera dans le triangle 
            
            Returns:    
                bool: renvoie si le point est dans le triangle
            """
            return e(v3, v1, p) > 0 and \
                   e(v2, v3, p) > 0 and \
                   e(v1, v2, p) > 0 or  \
                   e(v3, v1, p) < 0 and \
                   e(v2, v3, p) < 0 and \
                   e(v1, v2, p) < 0

        #  Borne sur lequel est défini le triangle
        xmin = round(min(tri.v1.x, tri.v2.x, tri.v3.x))
        xmax = round(max(tri.v1.x, tri.v2.x, tri.v3.x) + 1)
        ymin = round(min(tri.v1.y, tri.v2.y, tri.v3.y))
        ymax = round(max(tri.v1.y, tri.v2.y, tri.v3.y) + 1)

        #  Rempli avec le caractère donné le seulement l'intérieur du triangle
        #   et si le triangle est compris dans l'écran
        for y in range(ymin, ymax):
            if 0 <= y < self.height:
                for x in range(xmin, xmax):
                    if 0 <= x < self.width:
                        pos = lb_math.Vec2(x, y)

                        if est_dans_le_triangle(tri.v1, tri.v2, tri.v3, pos):
                            self.put_pixel(pos, char)

    def clip(self: 'MoteurGraphique', triangle: lb_math.Triangle3D,
             cam_pos: lb_math.Vec3,
             plane_normal: lb_math.Vec3) -> list[lb_math.Triangle3D]:
        """
            Clipping sous la forme du near clipping plane

            Explication;
                À la place de définir un plan face à la camera (le plan représente par !) 
                Nous allons le décaler.

        Camera    !                           
                  !                                  
                  !                                 
                  !                        
                  !                               
            oO    !    +-----------------------------+                                        
        +-----+   !       -                          |
        |      |/|!          -                       |   
        |      |\|!              -                   |        
        +------+  !                  -               |        
                  !                      -           |        
                  !                          -       |        
                  !                              -   |        
                  !                                  + 
                                         
            Il est donc décalé de la camera comme ceci donc si un sommet 
                et en dehors de ce plan, il faut le coupé 

        
        Camera               !                
                             !                       
                             !                      
                             !             
                             !                    
            oO        +------!-----------------------+                                        
        +-----+          -   !                       |
        |      |/|           -                       |   
        |      |\|           !   -                   |        
        +------+             !       -               |        
                             !           -           |        
                             !               -       |        
                             !                   -   |        
                             !                       + 
                             !            

                    

       Camera                !                
                             !                       
                             !                      
                             !             
                             !                    
            oO               !-----------------------+                                        
        +-----+              !                       |
        |      |/|           -                       |   
        |      |\|           !   -                   |        
        +------+             !       -               |        
                             !           -           |        
                             !               -       |        
                             !                   -   |        
                             !                       + 
                             ! 

            Une fois le découpage du point du triangle hors plan fait,  
                Il faut que le triangle soit toujours visible.
                Pour ça, nous allons recrée plusieurs sous triangle


      Camera                !                
                             !                       
                             !                      
                             !             
                             !                    
            oO               !-----------------------+                                        
        +-----+              !     _          -      |
        |      |/|           -                       |   
        |      |\|           !   -                   |        
        +------+             !       -               |        
                             !           -           |        
                             !               -       |        
                             !                   -   |        
                             !                       + 
                             !            

        Une fois les deux triangles reformés, il y a plus de problèmes seulement ici, 
        
        il manque un seul sommet, mais s'il n'en manque pas, on affiche tout, 
        mais s'il manque tous les sommets, on affiche rien.
        S'il en manque deux :
            On supprime toute la partie non-visible (partie remplie de / ), 
                puis on voit un nouveau triangle apparaître, 
                    on prend ce triangle-là comme nouveau triangle.

                  Camera                !                
                             !                       
                             !                      
                      +------!----------+             
                      |//////!       -            
            oO        |//////!    -                                   
        +-----+       |//////! -                   
        |      |/|    |/////-!                           
        |      |\|    |//-   !                               
        +------+      +      !                               
                             !                               
                             !                               
                             !                               
                             !                        
                             !            

        Et on garde les sommets sous une orientation dans le sens des aiguilles d'une montre

        Args:
            self (MoteurGraphique): moteur graphique
            triangle (lb_math.Triangle3D): mon triangle
            cam_pos (lb_math.Vec3): position de la camera
            plane_normal (lb_math.Vec3): vecteur normal au plan du clipping (vue de la camera)

        Returns:
            list[lb_math.Triangle3D]: Liste de triangle à afficher
        """

        def in_z(
            plane_normal: lb_math.Vec3, plane_point: lb_math.Vec3,
            tri: lb_math.Triangle3D
        ) -> tuple[list[lb_math.Vec3], list[lb_math.Vec3], bool]:
            """ 
                Renvoie une liste de triangles à l'intérieur et l'extérieur de notre plan

                   !                
                   !                       
            out[]  !        in_t[]                     
                   !             
                   !                    
            +------!-----------------------+                                        
               -   !                       |
                   -                       |   
                   !   -                   |        
                   !       -               |        
                   !           -           |        
                   !               -       |        
                   !                   -   |        
                   !                       + 
                   !            
            
                Pour savoir ca, il faut faire le produit scalaire entre le point sur notre plan 
                    ainsi que chacun des points du triangles
                si le resutlat est positif, le point est dans notre plan (int_t[]), 
                    sinon le point est pas visible (out[])
                
                calcul: v.n = ||v||*||n||*cos(a)

            Args:
                plane_normal (lb_math.Vec3): vecteur du plan normal
                plane_point (lb_math.Vec3): vecteur du point
                tri (lb_math.Triangle3D): le triangle a tester

            Returns:
                tuple[list[lb_math.Vec3], list[lb_math.Vec3], bool]: tuple avec la liste de 
                    triangles à l'intérieur et extérieur de la région 
                        puis un test si vert1 * vert 2 plus grand que 0 
                        
            """

            out = []
            in_t = []

            # Tester pour chaque point le produit scalaire
            vert1 = plane_normal.dot(plane_point - tri.v1)
            vert2 = plane_normal.dot(plane_point - tri.v2)
            vert3 = plane_normal.dot(plane_point - tri.v3)

            # Mettre dans la liste out ou in_t selon le résultat du test
            out.append(tri.v1) if vert1 > 0 else in_t.append(tri.v1)
            out.append(tri.v2) if vert2 > 0 else in_t.append(tri.v2)
            out.append(tri.v3) if vert3 > 0 else in_t.append(tri.v3)

            return out, in_t, vert1 * vert2 > 0

        # znear position du point sur le plan
        z_near = cam_pos + const.DISTANCE_CAMERA_PLAN * plane_normal
        # out point en dehors du plan, in point dans notre plan
        out, in_, is_inverted = in_z(plane_normal, z_near, triangle)

        #  tester toute les conditions,
        #   s'il n'y a aucun des points visibles,
        #   s'il y a tous les points visibles,
        #   s'il n'y a qu'un point visible,
        #   s'il n'y a que deux points visibles,
        if len(out) == 0:
            return [triangle]  # Prendre tout le triangle
        if len(out) == 3:
            return []  # Rejeter le triangle
        if len(out) == 1:
            collision0 = plane_normal.line_plane_intersection(
                z_near, out[0], in_[0])
            collision1 = plane_normal.line_plane_intersection(
                z_near, out[0], in_[1])

            if is_inverted:
                return [
                    lb_math.Triangle3D(collision1, in_[1], collision0),
                    lb_math.Triangle3D(collision0, in_[1], in_[0])
                ]
            return [
                lb_math.Triangle3D(collision0, in_[0], collision1),
                lb_math.Triangle3D(collision1, in_[0], in_[1])
            ]

        if len(out) == 2:
            collision0 = plane_normal.line_plane_intersection(
                z_near, out[0], in_[0])
            collision1 = plane_normal.line_plane_intersection(
                z_near, out[1], in_[0])

            if is_inverted:
                return [
                    lb_math.Triangle3D(collision0, in_[0], collision1),
                ]
            return [
                lb_math.Triangle3D(collision0, collision1, in_[0]),
            ]

    def put_mesh(self: 'MoteurGraphique', mesh: list[lb_math.Triangle3D],
                 cam: Camera, light_source: LightSource) -> None:
        """ 
            Pose plusieurs triangles par rapport à la camera, et affiche les triangles le clipping 
                (pour avoir les triangles du second plan qui ne se mettent pas sur le triangle du 
                    premier plan)


        Args:
            self (MoteurGraphique): Moteur graphique
            mesh (list[lb_math.Triangle3D]): Liste de triangle 3d a afficher
            cam (Camera): Notre camera 
            light_source (LightSource): La lumiere
        """

        # triangle: Triangle3D
        def distance_triangle_cam(triangle) -> float:
            """
                La distance entre chaque triangle avec la camera.


                pour faire :
        Camera                
                                  
                        !            
                        !           
                        !         \   
                        !          \  
            oO          !           \     /            
        +-----+         !        |   \   /  
        |      |/|      !        |    \ / 
        |      |\|      !        |     /      
        +------+        !        |    /       
                        !        |   /        
                        !           /         
                        !          /         
                        !         /   
                        !
                        !
     
            Qui donnera sur l'affichage :

                        !            
                        !           
                        \         \   
                        \          \  
            oO          \           \     /            
        +-----+         |        |   \   /  
        |      |/|      |        |    \ / 
        |      |\|      |        |     /      
        +------+        |        |    /       
                        |        |   /        
                        /           /         
                        /          /         
                        /         /   
                        !
                        !
                  

            Args:
                triangle (Triangle3D): Le triangle à tester

            Returns:
                float: La distance entre la camera et le triangle
            """
            # vecteur de distance
            position = (1 / 3) * (triangle.v1 + triangle.v2 +
                                  triangle.v3) - cam.position
            return position.lenght()

        # tri des triangles par rapport à la distance avec la camera
        #   (voir def distance_triangle_cam)
        mesh.sort(key=distance_triangle_cam, reverse=True)
        look_at = cam.get_look_at_direction()

        # poser tous les triangles de la liste de triangles
        for triangle in mesh:

            clipped_triangle_list = self.clip(triangle, cam.position, look_at)

            for clipped_triangle in clipped_triangle_list:
                line1 = clipped_triangle.v2 - clipped_triangle.v1
                line2 = clipped_triangle.v3 - clipped_triangle.v1
                surface_normal = line1.cross_prod(line2)
                """
                    pointe vers la camera  | point pas vers la camera                                                           
                                /\                    /\                   
                                 \         +          /                    
                                  \     -     -      /                      
                                   \ -           -  /                                  
            oO                    -                 -                                                        
        +-----+                -                       -                                     
        |      |/|          +                             +                
        |      |\|             -                       -                                                  
        +------+                  -                 -                                                    
                                  /  -           -  \                       
                                 /      -     -      \                        
                                /          +          \                    
                               \/                     \/                   
                                                                          
                    pointe vers la camera  | point pas vers la camera                                                           
                
                Si ça pointe vers la camera, on garde le triangle, sinon on ne le garde pas



                Pointer vers la camera signifie :
                    Que l'angle entre la camera et un point donné est supérieur ou eagle a 90°.
                                       ∧
                                        \
                                        /\ 
                                  >90° |  \                
                                        \  ~+                              
                                      ~ -     -                            
                                  ~  -           -                                    
            oO               ~    -                 -                                                        
        +-----+         ~      -                       -                                     
        |      |/|~          +                             +                
        |      |\|             -                       -                                                  
        +------+                  -                 -                                                    
                                     -           -                         
                                        -     -                              
                                           +                              

                                           Donc visible


                                      ∧
                                        \
                                         \ 
                                         /\                
                                        /  +                              
                              < 90°    |-  ~  -                            
                                     - \  ~      -                                    
                                  -     \~          -                                                        
                               -        ~              -                                     
                            +          ~                  +                
                               -      ~                -                                                  
                                  -  ~              -                                                    
                                    ~-           -                         
                                   ~    -     -                              
                                  ~        +                              
                                 ~           
                    oO          ~       
                    +-----+    ~            
                    |      |/|~            
                    |      |\|
                    +------+            
                            
                                 
                                 Donc pas visible            
                """

                if surface_normal.dot(clipped_triangle.v1 - cam.position) < 0:
                    #  calculer la lumière par rapport au triangle et choisir le meilleur
                    #   caractère en conséquent
                    #     (les caractères sont moins lumineux au plus lumineux.)
                    light_str: str = light_source.diffuse_light(
                        surface_normal, clipped_triangle.v1)
                    # poser les triangles par rapport à la camera
                    self.put_triangle(
                        clipped_triangle.translate(
                            -1 * cam.position).rotation_y(cam.yaw).rotation_x(
                                cam.pitch).projection(
                                    cam.focal_lenth).to_screen(), light_str)
