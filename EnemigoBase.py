import time
import pygame
import random
from Constantes import *

class EnemigoBase(pygame.sprite.Sprite):

    def __init__(self, px, py, ancho, alto, px_rect, py_rect, velocidad, velocidad_ataque, vida, offset_x_rect_ataque, offset_y_rect_ataque, ancho_rect_ataque, alto_rect_ataque):
        super().__init__()

        self.px = px
        self.py = py
        self.px_rect = px_rect
        self.py_rect = py_rect
        self.velocidad = velocidad
        self.velocidad_ataque = velocidad_ataque
        self.vida = vida
        self.offset_x_rect_ataque = offset_x_rect_ataque
        self.offset_y_rect_ataque = offset_y_rect_ataque
        self.ancho_rect_ataque = ancho_rect_ataque
        self.alto_rect_ataque = alto_rect_ataque

        # Rectangulo inicia en la posicion correcta para ajustar el cuadrado de colision:
        self.rect = pygame.Rect(px_rect, py_rect, ancho, alto)

        self.animaciones_base = {
            "caminar": [],
            "atacar": [],
            "danio": [],
            "morir": []
        }

        self.estado = "caminar"
        self.image = None
        self.contImagenes = 0
        self.atacando = False
        self.contador_animacion_ataques = 0
        self.ataque_rect = pygame.Rect(0, 0, 0, 0)

        # Nueva variable para controlar si el enemigo está en una pausa después de recibir daño
        self.en_danio = False
        self.cont_en_danio = 0
        self.muerto = False
        self.contador_animacion_muerte = 0

        # Sonido Personaje
        self.canal3 = pygame.mixer.Channel(3)
        self.sonido_muerte = pygame.mixer.Sound(SONIDO_MUERTE_E)
        self.sonido_muerte.set_volume(0.7)

        # Tiempo del último daño recibido
        self.ultimo_dano = 0

    # Metodo para cargar los sprites para caminar y atacar de los enemigos
    def cargar_animaciones(self, caminar, atacar, danio, morir):
        self.animaciones_base["caminar"] = [pygame.image.load(img).convert_alpha() for img in caminar]
        self.animaciones_base["atacar"] = [pygame.image.load(img).convert_alpha() for img in atacar]
        self.animaciones_base["danio"] = [pygame.image.load(img).convert_alpha() for img in danio]
        self.animaciones_base["morir"] = [pygame.image.load(img).convert_alpha() for img in morir]

        self.image = self.animaciones_base["caminar"][0]

    # Metodo para actualizar las animaciones
    def actualizar_animaciones(self):
        frames = self.animaciones_base[self.estado]
        self.image = frames[self.contImagenes % len(frames)]
        self.contImagenes += 1

    # Metodo para realizar ataque automático cada tiempo random
    def atacar(self):
        if not self.atacando and random.random() < self.velocidad_ataque:
            self.estado = "atacar"
            self.atacando = True
            self.contador_animacion_ataques = 0

            ataque_offset_x = self.offset_x_rect_ataque
            ataque_offset_y = self.offset_y_rect_ataque
            ataque_width = self.ancho_rect_ataque
            ataque_height = self.alto_rect_ataque

            self.ataque_rect = pygame.Rect(
                self.px - ataque_offset_x,
                self.py + self.rect.height - ataque_offset_y,
                ataque_width,
                ataque_height
            )

        elif self.atacando:
            self.contador_animacion_ataques += 1
            if self.contador_animacion_ataques >= len(self.animaciones_base["atacar"]):
                self.atacando = False
                self.estado = "caminar"

    # Metodo para que el enemigo reciba daño (con pausa de 1 segundo)
    def quitar_vida(self, danio):
        if time.time() - self.ultimo_dano >= 0.4:  # Solo puede recibir daño si ha pasado 1 segundo
            self.vida -= danio
            if self.vida <= 0:
                self.estado = "morir"
                self.muerto = True
                if not self.canal3.get_busy():
                    self.canal3.play(self.sonido_muerte)
                self.rect = pygame.Rect(0, 0, 0, 0)
                self.ataque_rect = pygame.Rect(0, 0, 0, 0)
                return True
            else:
                self.estado = "danio"
                self.ataque_rect = pygame.Rect(0, 0, 0, 0)
                self.en_danio = True
                self.cont_en_danio = 0
                # Registrar el momento en que el enemigo recibe daño
                self.ultimo_dano = time.time()
                return False

    # Metodo de movimiento
    def mover(self):
        if self.estado == "caminar":
            self.ataque_rect = pygame.Rect(0, 0, 0, 0)
            self.px -= self.velocidad
            self.px_rect -= self.velocidad
            self.rect.topleft = (self.px_rect, self.py_rect)

            if self.rect.right < 0:
                self.kill()

    # Metodo update para manejar los updates desde el grupo en el nivel
    def update(self):
        if self.muerto:  # Verificar si el enemigo está muerto
            if self.contador_animacion_muerte >= len(self.animaciones_base["morir"]):
                self.kill()  # Eliminar el enemigo después de la animación de muerte
            else:
                self.contador_animacion_muerte += 1
                self.estado = "morir"  # Mantener el estado de muerte

        elif self.en_danio:
            if self.cont_en_danio >= len(self.animaciones_base["danio"]):
                self.en_danio = False
                self.estado = "caminar"
            else:
                self.cont_en_danio += 1

        else:
            self.mover()
            self.atacar()

        self.actualizar_animaciones()

    # Metodo para dibujar al enemigo
    def dibujar(self, pantalla):
        pantalla.blit(self.image, (self.px, self.py))
        if self.rect is not None:
            pygame.draw.rect(pantalla, VERDE, self.rect, 2)
        if self.ataque_rect is not None:
            pygame.draw.rect(pantalla, ROJO, self.ataque_rect, 2)