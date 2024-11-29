import pygame
from Constantes import *
import random

class Enemigo1(pygame.sprite.Sprite):

    def __init__(self, px, py):

        super().__init__()
        self.px = px
        self.py = py
        self.rect = pygame.Rect(self.px, self.py, ANCHO_ENEMIGO1, ALTURA_ENEMIGO1)
        self.contador_tiempo_ataques = 0
        self.tiempo_entre_ataques = random.randrange(20,60)

        self.caminaizquierda = [pygame.image.load(f"imagenes/caminar/andar{i + 1}I.png").convert_alpha() for i in range(8)]

        self.contador_animacion_ataques = 0
        self.atacando = False
        self.cuenta_imagenes = 0
        self.direccion = False

        # Aseguramos que el sprite tiene un atributo image
        self.image = self.caminaizquierda[0]  # Asignamos la primera imagen de caminar a la imagen inicial

    def ejecutarEnemigo1(self, pantalla):

        self.atacarAleatorio()
        self.mover()
        self.dibujar(pantalla)

    def atacarAleatorio(self):

        if self.contador_tiempo_ataques < self.tiempo_entre_ataques:
            self.contador_tiempo_ataques += 1
        else:
            self.contador_tiempo_ataques = 0
            self.tiempo_entre_ataques = random.randrange(20, 60)
            self.atacando = True


        if self.atacando:
            if self.contador_animacion_ataques < TIEMPO_ANIMACION_ATAQUE:
                self.contador_animacion_ataques += 1
            else:
                self.contador_animacion_ataques = 0
                self.atacando = False

    def mover(self):

        if self.px > - 1000:
            self.px = self.px - VELOCIDAD_ENEMIGO1 + random.randrange(-40,40)

        self.rect.topleft = (self.px + CENTRO_X_CUADRADO, self.py + CENTRO_Y_CUADRADO)

    def dibujar(self, pantalla):

        # Animación según la dirección
        if self.cuenta_imagenes >= 8:
            self.cuenta_imagenes = 0

        if not self.atacando:
            self.image = self.caminaizquierda[self.cuenta_imagenes // 1]  # Actualizar la imagen
            pantalla.blit(self.image, (int(self.px), int(self.py)))
            pygame.draw.rect(pantalla, (0, 255, 0), self.rect, 2)

        if self.atacando:
            self.image = self.caminaizquierda[self.cuenta_imagenes // 1]  # Actualizar la imagen
            pantalla.blit(self.image, (int(self.px), int(self.py)))
            pygame.draw.rect(pantalla, (255, 0, 0), self.rect, 2)

        self.cuenta_imagenes += 1







