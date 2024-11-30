from pygame.sprite import Sprite

import Constantes
from Constantes import *
from pygame.locals import *

from Enemigo2 import Enemigo2
from Personaje import *
from Enemigo1 import *

class Lvl1(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        # Variables de configuración
        self.reloj = pygame.time.Clock()
        self.ejecutar = True

        # Configuración de la pantalla
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("LVL 1 - " + NOMBRE_JUEGO)
        self.icono = pygame.image.load(ICONO_JUEGO)
        pygame.display.set_icon(self.icono)
        self.fondo = pygame.image.load(FONDO_JUEGO_LVL1)

        # Grupo para enemigos, donde manejaremos los diferentes
        # enemigos existentes:
        self.enemigos = pygame.sprite.Group()

        # Contador puntos:
        self.contador_Puntos = 0

        # Musica fondo
        pygame.mixer.music.load(MUSICA_LVL1)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.8)

        # Personaje e inicializacion primer enemigo:
        self.personaje = Personaje(POSICION_INICIAL_X, POSICION_INICIAL_Y)


    def generar_enemigo(self):
        tipo_elegido = random.choice([Enemigo1, Enemigo2])
        altura_y = self.generador_y_aleatorio()
        nuevo_enemigo = tipo_elegido(next(altura_y))
        self.enemigos.add(nuevo_enemigo)


    def generador_y_aleatorio(self):
        contador = 0
        while True:
            yield contador
            contador = random.randrange(-70, 100)

    # Generador para generar tiempo aleatorio entre 150 y 300 frames, para la
    # generacion de enemigos:
    def generador_tiempo_aleatorio(self):
        contador = 0
        while True:
            yield contador
            contador = random.randrange(20, 50)


    #Eventos de usuario y de teclado:
    def eventos(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.ejecutar = False

        # Captura si pulsamos alguna tecla:
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            self.ejecutar = False

        # Ejecuta las acciones del personaje en pantalla:
        self.personaje.mover(keys, ANCHO_PANTALLA, ALTO_PANTALLA)


    # Metodo para entrar en el bucle del LVL1:
    def ejecutar_lvl1(self):

        # Asignamos el generador a una variable para usarlo:
        tiempo_aleatorio = self.generador_tiempo_aleatorio()
        # Para que no empiece en valor 0, ejecutamos una vez next:
        nuevo_tiempo = next(tiempo_aleatorio)
        #Contador auxiliar que ira aumentando para controlar el tiempo de generacion aleatoria:
        contador_entre_enemigos = 0

        #
        fuente_puntos = pygame.font.SysFont("Arial", 24)

        while self.ejecutar:

            self.reloj.tick(FPS)

            # Comprueba si ha pasado el tiempo minimo para generar otro enemigo
            if contador_entre_enemigos < nuevo_tiempo :
                contador_entre_enemigos += 1
            else:

                # Si ha pasado el tiempo suficiente, genera otro nuevo tiempo al azar
                # pone contador a 0 y genera al enemigo.
                nuevo_tiempo = next(tiempo_aleatorio)
                contador_entre_enemigos = 0
                self.generar_enemigo()

            # Pinta fondo:
            self.pantalla.blit(self.fondo, (0, 0))

            # Ejecuta los eventos y updates
            self.eventos()
            self.enemigos.update()

            # Dibuja los personajes:
            self.personaje.dibujar(self.pantalla)
            for enemigo in self.enemigos:
                enemigo.dibujar(self.pantalla)

            # Dibujamos en pantalla el texto actualizado de la puntuacion
            puntos = fuente_puntos.render(f"Puntos: {self.contador_Puntos}", True, (255, 255, 255))
            self.pantalla.blit(puntos, (X_TEXTO_PUNTOS, Y_TEXTO_PUNTOS))

            # Bucle para comprobar si hay colisiones con enemigos:
            for enemigo in self.enemigos:
                if self.personaje.ataque_rect is not None:
                    if self.personaje.ataque_rect.colliderect(enemigo.rect):
                        enemigo.quitar_vida(20)
                        self.contador_Puntos += 10

                if enemigo.rect.colliderect(self.personaje.rect):
                    muerte = self.personaje.danio_jugador(25)
                    if muerte:
                        pygame.quit()



            # Actualiza el display:
            pygame.display.flip()

        pygame.quit()

        #if keys[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
            #pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.10)


        #if keys[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
            #pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.10)

