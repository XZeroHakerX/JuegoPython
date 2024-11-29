from pygame.sprite import Sprite

import Constantes
from Constantes import *
from pygame.locals import *
from Personaje import *
from Enemigo1 import *

class Principal(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        # Variables de configuración
        self.RELOJ = pygame.time.Clock()

        # Configuración de la pantalla
        self.PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("LVL 1 - " + NOMBRE_JUEGO)
        self.icono = pygame.image.load(ICONO_JUEGO)
        pygame.display.set_icon(self.icono)
        self.fondo = pygame.image.load(FONDO_JUEGO_LVL1)

        # Variable aleatorias emnemigos

        self.contador_entre_enemigos = 0
        self.tiempo_aleatorio = random.randrange(150, 300)
        self.enemigos = pygame.sprite.Group()

        #Contador puntos:
        self.contador_Puntos = 0

        # Musica fondo
        pygame.mixer.music.load(MUSICA_LVL1)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.8)

        #Personaje e inicializacion:
        self.personaje = Personaje(POSICION_INICIAL_X, POSICION_INICIAL_Y)
        self.enemigo1 = Enemigo1(POSICION_INICIAL_X_ENEMIGO1, POSICION_INICIAL_Y_ENEMIGO1 + random.randrange(-75, 40))

        self.enemigos.add(self.enemigo1)


    def ejecutar(self):

        self.ejecutar = True

        while self.ejecutar:
            self.RELOJ.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.ejecutar = False

            if self.contador_entre_enemigos < self.tiempo_aleatorio:
                self.contador_entre_enemigos += 1
            else:
                self.enemigo1.kill()
                self.contador_entre_enemigos = 0
                self.enemigo1 = Enemigo1(POSICION_INICIAL_X_ENEMIGO1, POSICION_INICIAL_Y_ENEMIGO1 + random.randrange(-75, 40))
                self.enemigos.add(self.enemigo1)
                self.tiempo_aleatorio = random.randrange(150, 400)

            #Pinta fondo:
            self.PANTALLA.blit(self.fondo, (0, 0))

            #Captura si pulsamos alguna tecla:
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                self.ejecutar = False

            #Ejecuta las acciones del personaje en pantalla:
            self.personaje.mover(keys,ANCHO_PANTALLA, ALTO_PANTALLA)
            self.personaje.dibujar(self.PANTALLA)


            self.enemigo1.ejecutarEnemigo1(self.PANTALLA)

            for enemigo in self.enemigos:
                if self.personaje.rect.colliderect(enemigo.rect):
                    #enemigo.morir(self.PANTALLA)
                    print("¡Colisión detectada entre el personaje y el enemigo!")
                    self.contador_Puntos += 1

            self.enemigos.update()
            #self.enemigos.draw(self.PANTALLA)

            # Actualiza el display:
            pygame.display.flip()

        pygame.quit()

        #if keys[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
            #pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.10)


        #if keys[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
            #pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.10)

