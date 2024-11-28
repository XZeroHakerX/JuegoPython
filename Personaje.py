from Constantes import *
import pygame

class Personaje:
    def __init__(self, px, py):

        self.px = px
        self.py = py
        self.velocidad = VELOCIDAD_PERSONAJE
        self.ancho = ANCHO_MOVIMIENTO_MAX
        self.altura_salto = 20
        self.en_salto = False

        #Variables de movimiento
        self.idle = True
        self.izquierda = False
        self.derecha = False
        self.arriba = False
        self.abajo = False
        self.cuentapasos = 0

        #Animaciones de personaje
        self.idleAni = [pygame.image.load(f"imagenes/Idle/Idle{i + 1}.png").convert_alpha() for i in range(9)]
        self.saltoAni = [pygame.image.load(f"imagenes/salto{i + 1}.png").convert_alpha() for i in range(2)]
        self.caminaderecha = [pygame.image.load(f"imagenes/caminar/andar{i + 1}.png").convert_alpha() for i in range(8)]
        self.caminaizquierda = [pygame.image.load(f"imagenes/caminar/andar{i + 1}I.png").convert_alpha() for i in range(8)]

        #Sonido Personaje
        self.canal0 = pygame.mixer.Channel(0)
        self.sonido_salto = pygame.mixer.Sound(f"sonidos/Sonido_Salto.mp3")
        self.sonido_salto.set_volume(0.7)




    def mover(self, keys, limite_ancho, limite_alto):
        if keys[pygame.K_a] and self.px > self.velocidad:
            self.px -= self.velocidad
            self.izquierda = True
            self.derecha = False
            self.idle = False

        elif keys[pygame.K_d] and self.px < limite_ancho - self.velocidad - self.ancho:
            self.px += self.velocidad
            self.derecha = True
            self.izquierda = False
            self.idle = False
        else:
            self.izquierda = False
            self.derecha = False
            self.idle = True

        if keys[pygame.K_w] and self.py > 360 and not self.en_salto:
            self.py -= self.velocidad
            self.arriba = True
            self.abajo = False
            self.idle = False
        elif keys[pygame.K_s] and self.py < 450 and not self.en_salto:
            self.py += self.velocidad
            self.abajo = True
            self.arriba = False
            self.idle = False
        else:
            self.abajo = False
            self.arriba = False
            self.idle = True


        if not self.en_salto:
            if keys[pygame.K_SPACE]:
                if not self.canal0.get_busy():
                    self.canal0.play(self.sonido_salto)
                self.en_salto = True
                self.altura_salto = ALTURA_SALTO
        else:
            if self.altura_salto >= -ALTURA_SALTO:
                self.py -= (self.altura_salto * abs(self.altura_salto)) * 0.5
                self.altura_salto -= 1
            else:
                self.en_salto = False
                self.altura_salto = ALTURA_SALTO




    def dibujar(self, pantalla):
        # Animación según la dirección
        if self.cuentapasos >= 8:
            self.cuentapasos = 0

        if self.izquierda and not self.en_salto:
            pantalla.blit(self.caminaizquierda[self.cuentapasos // 1], (int(self.px), int(self.py)))

        elif self.derecha and not self.en_salto:
            pantalla.blit(self.caminaderecha[self.cuentapasos // 1], (int(self.px), int(self.py)))

        elif self.arriba or self.abajo:
            if not self.derecha and not self.izquierda:
                pantalla.blit(self.caminaderecha[self.cuentapasos // 1], (int(self.px), int(self.py)))

        elif self.en_salto + 1 >= 2:
            pantalla.blit(self.saltoAni[1], (int(self.px), int(self.py)))

        else:  # Animación idle
            pantalla.blit(self.idleAni[self.cuentapasos // 1], (self.px, self.py))

        self.cuentapasos += 1