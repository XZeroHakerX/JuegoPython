import pygame
import random
from Constantes import *


class EnemigoBase(pygame.sprite.Sprite):

    def __init__(self, px, py, ancho, alto, px_rect, py_rect, velocidad, velocidad_ataque, vida):

        super().__init__()

        # Atributos de enemigo base, posicion de salida x, y
        # velocidad, y el rectangulo para las colisiones:
        self.px = px
        self.py = py
        self.px_rect = px_rect
        self.py_rect = py_rect
        self.velocidad = velocidad
        self.velocidad_ataque = velocidad_ataque
        self.vida = vida

        # Rectangulo inicia en la posicion correcta para ajustar el cuadrado de colision:
        self.rect = pygame.Rect(px_rect, py_rect, ancho, alto)

        ## Diccionario?# Variable donde se van a cargar las imagenes para las animaciones:
        self.animaciones_base = {
            "caminar": [],
            "atacar": []
        }

        # Variable para controlar las animaciones:
        self.estado = "caminar"

        # Imagen donde se iran reproduciendo los sprites
        self.image = None

        # Cont. para imagenes
        self.contImagenes = 0

        # Control de ataque
        self.atacando = False
        self.contador_animacion_ataques = 0



    # Metodo para cargar los sprites para caminar y atacar de los enemigos:
    def cargar_animaciones(self, caminar, atacar):
        # Guardamos en un
        self.animaciones_base["caminar"] = [pygame.image.load(img).convert_alpha() for img in caminar]
        self.animaciones_base["atacar"] = [pygame.image.load(img).convert_alpha() for img in atacar]

        # Ponemos la primera imagen de caminar como default:
        self.image = self.animaciones_base["caminar"][0]



    # Metodo para actualizar las animaciones:
    def actualizar_animaciones(self):
        #Recuperamos los sprites segun el estado del personaje:
        frames = self.animaciones_base[self.estado]
        # Damos a la imagen el sprite que le corresponde segun el contador y le sumamos 1:
        self.image = frames[self.contImagenes % len(frames)]
        self.contImagenes += 1

    # Metodo para realizar ataque automatico cada tiempo random
    def atacar(self):

        # Si no esta atacando y sale la probabilidad, el enemigo ataca:
        if not self.atacando and random.random() < self.velocidad_ataque:
            self.estado = "atacar"
            self.atacando = True
            self.contador_animacion_ataques = 0
        # Mientras durea la animacion de ataque, suma 1 al contador:
        elif self.atacando:
            self.contador_animacion_ataques += 1
            #Cuando el contador pasa al numero de imagenes de ataque, reinicia
            if self.contador_animacion_ataques >= len(self.animaciones_base["atacar"]):
                self.atacando = False
                self.estado = "caminar"

    # Metodo de enemigos para recibir daño:
    def quitar_vida(self, danio):
        self.vida -= danio
        if self.vida <= 0:
            self.kill()


    # Metodo de movimiento:
    def mover(self):
        # Comprueba que el estado es andando, si ataca permanece quieto:
        if self.estado == "caminar":
            # Actualizacion de movimiento segun velocidad:
            self.px -= self.velocidad
            self.px_rect -= self.velocidad
            # Actualizacion del rectangulo para colisiones:
            self.rect.topleft = (self.px_rect, self.py_rect)

            # Cuando sale de la pantalla mata el objeto
            if self.rect.right < 0:
                self.kill()


    # Metodo update para manejar los updates desde el grupo en el nivel donde se esten generando:
    def update(self):

        self.mover()
        self.atacar()
        self.actualizar_animaciones()




    # Metodo para dibujar a los enemigos:
    def dibujar(self, pantalla):

        pantalla.blit(self.image, (self.px, self.py))

        # Opcional: Dibujar el rectángulo de colisión
        pygame.draw.rect(pantalla, VERDE if not self.atacando else ROJO, self.rect, 2)