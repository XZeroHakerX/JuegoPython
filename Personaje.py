from Constantes import *
import pygame

class Personaje:
    def __init__(self, px, py):
        super().__init__()
        self.px = px
        self.py = py
        self.velocidad = VELOCIDAD_PERSONAJE
        self.altura_salto = ALTURA_SALTO
        self.en_salto = False
        self.rect = pygame.Rect(self.px + CENTRO_X_CUADRADO , self.py + CENTRO_Y_CUADRADO, ANCHO_PERSONAJE, ALTURA_PERSONAJE)

        # Estados de personajes para transicion de animaciones
        self.estado = "idle"
        self.direccion = "derecha"

        # Animaciones de personaje en un diccionario:
        self.animaciones_personaje ={
            "idle": [pygame.image.load(f"imagenes/Idle/Idle{i + 1}.png").convert_alpha() for i in range(9)],
            "caminar_derecha": [pygame.image.load(f"imagenes/caminar/andar{i + 1}.png").convert_alpha() for i in range(8)],
            "caminar_izquierda": [pygame.image.load(f"imagenes/caminar/andar{i + 1}I.png").convert_alpha() for i in range(8)],
            "saltar": [pygame.image.load(f"imagenes/salto{i + 1}.png").convert_alpha() for i in range(2)],
            "atacar": [pygame.image.load(f"imagenes/salto{i + 1}.png").convert_alpha() for i in range(2)]
        }

        self.cuenta_imagenes = 0
        self.image = self.animaciones_personaje["idle"][0]


        # Sonido Personaje
        self.canal0 = pygame.mixer.Channel(0)
        self.sonido_salto = pygame.mixer.Sound(f"sonidos/Sonido_Salto.mp3")
        self.sonido_salto.set_volume(0.7)




    def mover(self, keys, limite_ancho, limite_alto, obstaculos=None):


        if obstaculos is None:
            obstaculos = []

        # Utilizamos dos variables nuevas para hacer la prediccion de movimiento y
        # saber si colisiona con algun objeto.
        nuevo_px = self.px
        nuevo_py = self.py

        # Si presionampos la tecla 'a' y la posicion es mayor que la velocidad,
        # movemos a la izquierda al personaje
        if keys[pygame.K_a] and self.px > self.velocidad:
            nuevo_px -= self.velocidad
            self.estado = "caminar"
            self.direccion = "izquierda"

        elif keys[pygame.K_d] and self.px < limite_ancho - self.velocidad - self.rect.width:
            nuevo_px += self.velocidad
            self.estado = "caminar"
            self.direccion = "derecha"
        else:
            self.estado = "idle"

        # Movimiento vertical del personaje con las limitacion es de movimiento:
        if keys[pygame.K_w] and self.py > LVL1_MAX_Y and not self.en_salto:
            nuevo_py -= self.velocidad
            self.estado = "caminar"
        elif keys[pygame.K_s] and self.py < LVL1_MIN_Y and not self.en_salto:
            nuevo_py += self.velocidad
            self.estado = "caminar"

        # Cuando el jugador toca el boton de salto, pasamos la variable a true y entra
        # en el metodo de salto
        if not self.en_salto and keys[pygame.K_SPACE]:
            self.en_salto = True
            if not self.canal0.get_busy():
                self.canal0.play(self.sonido_salto)

        if self.en_salto:
            if self.altura_salto >= -ALTURA_SALTO:
                nuevo_py -= (self.altura_salto * abs(self.altura_salto)) * 0.5
                self.altura_salto -= 1
            else:
                self.en_salto = False
                self.altura_salto = ALTURA_SALTO


        # Comprobacion de los obstaculos, genera un rectangulo provisional, y si ese toca con
        # algun obstaculo no actualiza la posicion:
        aux_rect = pygame.Rect(nuevo_px, nuevo_py, self.rect.width, self.rect.height)
        colisiona = any(aux_rect.colliderect(obstaculo.rect) for obstaculo in obstaculos)

        # Si no colisiona con nada puede seguir moviendose (Futura actualizacion)
        if not colisiona:
            self.px = nuevo_px
            self.py = nuevo_py
            # Actualizar el rectángulo del personaje
            self.rect.topleft = (self.px + CENTRO_X_CUADRADO, self.py + CENTRO_Y_CUADRADO)




    # Metodo para actualizar las imagenes que se muestran segun estado y posicion:
    def actualizar_animacion(self):
        if self.estado == "idle" and not self.en_salto:
            frame = self.animaciones_personaje["idle"]
        elif self.estado == "caminar" and self.direccion == "derecha" and not self.en_salto:
            frame = self.animaciones_personaje["caminar_derecha"]
        elif self.estado == "caminar" and self.direccion == "izquierda" and not self.en_salto:
            frame = self.animaciones_personaje["caminar_izquierda"]
        elif self.en_salto:
            if self.py < 0:
                frame = self.animaciones_personaje["saltar"][0]

            else:
                frame = self.animaciones_personaje["saltar"][1]
            self.image = frame
        else:
            frame = self.animaciones_personaje["idle"]

        if not self.en_salto:
            self.image = frame[self.cuenta_imagenes % len(frame)]
            self.cuenta_imagenes += 1



    def dibujar(self, pantalla):

        self.actualizar_animacion()
        pantalla.blit(self.image, (self.px, self.py))
        pygame.draw.rect(pantalla, ROJO, self.rect, 2)