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
        self.rect = pygame.Rect(self.px , self.py, ANCHO_PERSONAJE, ALTURA_PERSONAJE)

        #Variables de movimiento
        self.idle = True
        self.izquierda = False
        self.derecha = False
        self.arriba = False
        self.abajo = False
        self.cuenta_imagenes = 0

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

        #Utilizamos dos variables nuevas para hacer la prediccion de movimiento y
        #saber si colisiona con algun objeto.
        nuevo_px = self.px
        nuevo_py = self.py

        if keys[pygame.K_a] and self.px > self.velocidad:

            nuevo_px -= self.velocidad
            self.izquierda = True
            self.derecha = False
            self.idle = False

        elif keys[pygame.K_d] and self.px < limite_ancho - self.velocidad - self.ancho:
            nuevo_px += self.velocidad
            self.derecha = True
            self.izquierda = False
            self.idle = False
        else:
            self.izquierda = False
            self.derecha = False
            self.idle = True

        if keys[pygame.K_w] and self.py > 360 and not self.en_salto:
            nuevo_py -= self.velocidad
            self.arriba = True
            self.abajo = False
            self.idle = False
        elif keys[pygame.K_s] and self.py < 450 and not self.en_salto:
            nuevo_py += self.velocidad
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
                nuevo_py -= (self.altura_salto * abs(self.altura_salto)) * 0.5
                self.altura_salto -= 1
            else:
                self.en_salto = False
                self.altura_salto = ALTURA_SALTO

        # Comprobacion de los obstaculos:
        aux_rect = pygame.Rect(nuevo_px, nuevo_py, self.rect.width, self.rect.height)
       # colisiona = any(aux_rect.colliderect(obstaculo.rect) for obstaculo in obstaculos)

        #if not colisiona:
        self.px = nuevo_px
        self.py = nuevo_py

        # Actualizar el rectángulo del personaje
        self.rect.topleft = (self.px + CENTRO_X_CUADRADO, self.py + CENTRO_Y_CUADRADO)


    def dibujar(self, pantalla):

        # Animación según la dirección
        if self.cuenta_imagenes >= 8:
            self.cuenta_imagenes = 0
        
        if self.izquierda and not self.en_salto:
            pantalla.blit(self.caminaizquierda[self.cuenta_imagenes // 1], (int(self.px), int(self.py)))

        elif self.derecha and not self.en_salto:
            pantalla.blit(self.caminaderecha[self.cuenta_imagenes // 1], (int(self.px), int(self.py)))

        elif self.arriba or self.abajo:
            if not self.derecha and not self.izquierda:
                pantalla.blit(self.caminaderecha[self.cuenta_imagenes // 1], (int(self.px), int(self.py)))

        elif self.en_salto + 1 >= 2:
            pantalla.blit(self.saltoAni[1], (int(self.px), int(self.py)))

        else:  # Animación idle
            pantalla.blit(self.idleAni[self.cuenta_imagenes // 1], (self.px, self.py))

        if self.derecha or self.izquierda or self.idle or self.arriba or self.abajo:
            self.cuenta_imagenes += 1

        pygame.draw.rect(pantalla, (255, 0, 0), self.rect, 2)