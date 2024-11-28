import Constantes
from Constantes import *
from pygame.locals import *
from Personaje import *

class Principal:

    def __init__(self):

        # Variables de configuración
        self.RELOJ = pygame.time.Clock()

        # Configuración de la pantalla
        self.PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("LVL 1 - " + NOMBRE_JUEGO)
        self.icono = pygame.image.load(ICONO_JUEGO)
        pygame.display.set_icon(self.icono)
        self.fondo = pygame.image.load(FONDO_JUEGO_LVL1)

        # Musica fondo
        pygame.mixer.music.load(MUSICA_LVL1)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.8)

        #Personaje e inicializacion:
        self.personaje = Personaje(POSICION_INICIAL_X, POSICION_INICIAL_Y)


    def ejecutar(self):

        self.ejecutar = True

        while self.ejecutar:
            self.RELOJ.tick(FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.ejecutar = False

            #Pinta fondo:
            self.PANTALLA.blit(self.fondo, (0, 0))

            #Captura si pulsamos alguna tecla:
            keys = pygame.key.get_pressed()

            #Ejecuta las acciones del personaje en pantalla:
            self.personaje.mover(keys,ANCHO_PANTALLA, ALTO_PANTALLA)
            self.personaje.dibujar(self.PANTALLA)

            #Actualiza el display:
            pygame.display.update()

        pygame.quit()




        #if keys[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
            #pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.10)


        #if keys[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
            #pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.10)

