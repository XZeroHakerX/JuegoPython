import time

from Constantes import *
import pygame

class Personaje:
    def __init__(self, px, py):
        super().__init__()
        # Variables de personaje:
        self.px = px
        self.py = py
        self.velocidad = VELOCIDAD_PERSONAJE
        self.altura_salto = ALTURA_SALTO
        self.en_salto = False
        self.atacando = False
        self.vida = VIDA_INICIAL
        # Rectangulo de colisiones de personaje:
        self.rect = pygame.Rect(self.px + CENTRO_X_CUADRADO, self.py + CENTRO_Y_CUADRADO, ANCHO_PERSONAJE, ALTURA_PERSONAJE)

        # Estados de personajes para transicion de animaciones
        self.estado = "idle"
        self.direccion = "derecha"

        # DICCIONARIO de animaciones para personaje:
        self.animaciones_personaje = {
            "idle": [pygame.image.load(f"imagenes/pj/Idle/Idle{i + 1}.png").convert_alpha() for i in range(9)],
            "caminar_derecha": [pygame.image.load(f"imagenes/pj/caminar/andar{i + 1}.png").convert_alpha() for i in range(8)],
            "caminar_izquierda": [pygame.image.load(f"imagenes/pj/caminar/andar{i + 1}I.png").convert_alpha() for i in range(8)],
            "saltar": [pygame.image.load(f"imagenes/pj/salto{i + 1}.png").convert_alpha() for i in range(2)],
            "atacar_d": [pygame.image.load(f"imagenes/pj/atacar/ataque{i + 1}.png").convert_alpha() for i in range(1)],
            "atacar_i": [pygame.image.load(f"imagenes/pj/atacar/ataque{i + 1}I.png").convert_alpha() for i in range(1)],
            "danio": [pygame.image.load(f"imagenes/pj/danio/danio{i + 1}.png").convert_alpha() for i in range(2)],
            "morir": [pygame.image.load(f"imagenes/pj/muerte/morir{i + 1}.png").convert_alpha() for i in range(4)]
        }

        self.cuenta_imagenes = 0

        self.frame_actual_ataque = 0  # Agregado para llevar el control de los fotogramas de ataque
        self.image = self.animaciones_personaje["idle"][0]

        # Sonidos Personaje:
        self.canal1 = pygame.mixer.Channel(1)
        self.canal2 = pygame.mixer.Channel(2)
        self.sonido_salto = pygame.mixer.Sound(SONIDO_SALTO_PJ)
        self.sonido_salto.set_volume(0.7)
        self.sonido_danio = pygame.mixer.Sound(SONIDO_DANIO)
        self.sonido_danio.set_volume(0.6)
        self.sonido_ataque = pygame.mixer.Sound(SONIDO_ATAQUE)
        self.sonido_ataque.set_volume(0.6)

        # Rectángulo de colision del ataque del personaje
        self.ataque_rect = pygame.Rect(0, 0, 0, 0)

        # Contador para calcular 1 segundo desde el ultimo daño:
        self.ultimo_danio = 0

    def mover(self, keys, limite_ancho, obstaculos=None):
        if obstaculos is None:
            obstaculos = []

        # Utilizamos dos variables nuevas para hacer la predicción de movimiento y
        # saber si colisiona con algún objeto.
        nuevo_px = self.px
        nuevo_py = self.py

        # Movimiento horizontal:
        if keys[pygame.K_a] and self.px > self.velocidad and not self.atacando:
            nuevo_px -= self.velocidad
            self.estado = "caminar"
            self.direccion = "izquierda"
        elif keys[pygame.K_d] and self.px < limite_ancho - self.velocidad - self.rect.width and not self.atacando:
            nuevo_px += self.velocidad
            self.estado = "caminar"
            self.direccion = "derecha"
        else:
            self.estado = "idle"


        # Movimiento vertical:
        if keys[pygame.K_w] and self.py > LVL1_MAX_Y and not self.en_salto and not self.atacando:
            nuevo_py -= self.velocidad
            self.estado = "caminar"
        elif keys[pygame.K_s] and self.py < LVL1_MIN_Y and not self.en_salto and not self.atacando:
            nuevo_py += self.velocidad
            self.estado = "caminar"

        # Salto:
        if not self.en_salto and keys[pygame.K_SPACE] and not self.atacando:
            self.en_salto = True
            # Sonido de salto:
            self.canal1.play(self.sonido_salto)

        if self.en_salto and not self.atacando:
            if self.altura_salto >= -ALTURA_SALTO:
                nuevo_py -= (self.altura_salto * abs(self.altura_salto)) * 0.5
                self.altura_salto -= 1
            else:
                self.en_salto = False
                self.altura_salto = ALTURA_SALTO

        # Ataque 'L':
        if keys[pygame.K_l] and not self.atacando:
            self.atacando = True
            self.frame_actual_ataque = 0  # Resetear el frame de ataque al inicio
            self.cuenta_imagenes = 0

            if self.direccion == "derecha":
                self.estado = "atacar_d"
            elif self.direccion == "izquierda":
                self.estado = "atacar_i"

            self.atacar()

        elif self.atacando:
            animacion = self.animaciones_personaje[self.estado]

            if self.frame_actual_ataque < len(animacion):
                # Avanzar fotograma de la animacion
                self.frame_actual_ataque += 1

                # Activa el rect_ataque para solo un fotograma:
                if self.frame_actual_ataque == 1:
                    self.ataque_rect = self.direccion_ataque()
                else:
                    self.ataque_rect = pygame.Rect(0,0,0,0)
            # Cuando termina reinicia:
            else:
                self.frame_actual_ataque = 0
                self.atacando = False
                self.ataque_rect = pygame.Rect(0,0,0,0)
                self.estado = "idle"

        # Colision con los obstaculos, futura actualizacion para plataformas:
        aux_rect = pygame.Rect(nuevo_px, nuevo_py, self.rect.width, self.rect.height)
        colisiona = None  # any(aux_rect.colliderect(obstaculo.rect) for obstaculos in obstaculos)

        # Si no colisiona con nada, se actualiza la posicion
        if not colisiona:
            self.px = nuevo_px
            self.py = nuevo_py
            # Actualizar el rectángulo de colision
            self.rect.topleft = (self.px + CENTRO_X_CUADRADO, self.py + CENTRO_Y_CUADRADO)


    def atacar(self):

        # Sonido de ataque personaje:
        self.canal2.play(self.sonido_ataque)
        # Activamos el ataque y definimos el área de colision del ataque
        self.ataque_rect = self.direccion_ataque()


    def direccion_ataque(self):
        # Dependiendo de la direccion, generacion el rect_ataque para una direccion u otra:
        if self.direccion == "derecha":
            return pygame.Rect(self.px + self.rect.width + 50, self.py + self.rect.height - 150 // 4, 120, 15)
        elif self.direccion == "izquierda":
            return pygame.Rect(self.px - 100, self.py + self.rect.height - 150 // 4, 120, 15)


    # Metodo para actualizar las animaciones que se muestran según estado y posicion
    def actualizar_animacion(self):

        #Segun en el estado en el que se encuentre el personaje actualizara la imagen del mismo, con la
        # animacion que le corresponda segun la tirada de imagenes guardada:
        if self.estado == "danio":
            self.image = self.animaciones_personaje["danio"][self.cuenta_imagenes % len(self.animaciones_personaje["danio"])]
            self.cuenta_imagenes += 1
            return

        if self.estado == "idle" and not self.en_salto and not self.atacando:
            frame = self.animaciones_personaje["idle"]
        elif self.estado == "caminar" and self.direccion == "derecha" and not self.en_salto and not self.atacando:
            frame = self.animaciones_personaje["caminar_derecha"]
        elif self.estado == "caminar" and self.direccion == "izquierda" and not self.en_salto and not self.atacando:
            frame = self.animaciones_personaje["caminar_izquierda"]

        elif self.en_salto and not self.atacando:
            # Animacion de salto
            self.image = self.animaciones_personaje["saltar"][1 if self.py >= 0 else 0]
            return

        elif self.estado == "atacar_d" or self.estado == "atacar_i":

            # Intentamos asegurar que no salga de la animacion de ataque antes de lo que debe:
            frame = self.animaciones_personaje[self.estado]

            if self.cuenta_imagenes % 2 == 0:
                self.image = frame[self.cuenta_imagenes % len(frame)]
            self.cuenta_imagenes += 1
            return

        else:
            frame = self.animaciones_personaje["idle"]

        # Imagen del personaje si no esta saltando ni atacando
        if not self.en_salto and not self.atacando:
            self.image = frame[self.cuenta_imagenes % len(frame)]
            self.cuenta_imagenes += 1

    # Metodo para recibir daño y comprobar si a muerto o no:
    def danio_jugador(self, danio) -> bool:

        # Sonido de recibir daño
        self.canal1.play(self.sonido_danio)
        if time.time() - self.ultimo_danio >= 1:
            self.vida -= danio
            # Guardar el tiempo en que se recibio el daño
            self.ultimo_danio = time.time()
            # Cambiar el estado a "danio"
            self.estado = "danio"
            # Resetear el contador de animacion de daño
            self.cuenta_imagenes = 0
            return self.vida <= 0
        return False

    # Metodo para dibujar al personaje en pantalla y la vida del mismo:
    def dibujar(self, pantalla):
        self.actualizar_animacion()
        pantalla.blit(self.image, (self.px, self.py))

        # Dibujamos rect del personaje para DEBUG:
        pygame.draw.rect(pantalla, VERDE, self.rect, 2)

        # Dibujamos rect_ataque:
        if self.ataque_rect is not None:
            pygame.draw.rect(pantalla, ROJO, self.ataque_rect)

        # Mostrar la vida en pantalla:
        fuente_vida = pygame.font.SysFont("Arial", 40)
        texto_vida = fuente_vida.render(f"Vida: {self.vida}", True, ROJO)
        pantalla.blit(texto_vida, (X_TEXTO_VIDA, Y_TEXTO_VIDA))