from pygame.sprite import Sprite

import Constantes
from Constantes import *
from pygame.locals import *

from Enemigo3 import *
from Menu import *
from Enemigo2 import *
from Personaje import *
from Enemigo1 import *



# Clase Lvl1  Primer nivel del juego
class Lvl1(pygame.sprite.Sprite):

    def __init__(self, menu_enter):

        super().__init__()
        self.menu = menu_enter
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

        # Contador puntos del jugador:
        self.contador_Puntos = 0

        # Musica fondos
        pygame.mixer.music.load(MUSICA_LVL1)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.6)

        # Inicializacion del personaje:
        self.personaje = Personaje(POSICION_INICIAL_X, POSICION_INICIAL_Y)


    #generador de enemigos aleatorio:
    def generar_enemigo(self):
        tipo_elegido = random.choice([Enemigo1,Enemigo2,Enemigo3])
        nuevo_enemigo = tipo_elegido()
        self.enemigos.add(nuevo_enemigo)


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

        # Subimos y bajamos volumen:
        if keys[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.10)
        if keys[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.10)

        # Ejecuta las acciones del personaje en pantalla:
        self.personaje.mover(keys, ANCHO_PANTALLA, ALTO_PANTALLA)


    # Metodo para entrar en el bucle del LVL1:
    def ejecutar_lvl1(self):
        tiempo_aleatorio = self.generador_tiempo_aleatorio()
        nuevo_tiempo = next(tiempo_aleatorio)
        contador_entre_enemigos = 0

        fuente_puntos = pygame.font.SysFont("Arial", 30)
        fuente_victoria = pygame.font.SysFont("Arial", 50)

        while self.ejecutar:

            self.reloj.tick(FPS)

            # Generamos enemigos en intervalos aleatorios:
            if contador_entre_enemigos < nuevo_tiempo:
                contador_entre_enemigos += 1
            else:
                nuevo_tiempo = next(tiempo_aleatorio)
                contador_entre_enemigos = 0
                self.generar_enemigo()

            # Dibujamos enemigos y personaje
            self.pantalla.blit(self.fondo, (0, 0))
            self.eventos()
            self.enemigos.update()
            self.personaje.dibujar(self.pantalla)
            for enemigo in self.enemigos:
                enemigo.dibujar(self.pantalla)

            # Dibujamos los puntos del jugador
            puntos = fuente_puntos.render(f"{self.contador_Puntos} / {PUNTOS_GANAR_LVL1}", True, BLANCO)
            self.pantalla.blit(puntos, (X_TEXTO_PUNTOS, Y_TEXTO_PUNTOS))

            # Comprobacion de puntos para saber si se gano el nivel.
            # Si ganas ejecuta el evento de victoria:
            if self.contador_Puntos >= PUNTOS_GANAR_LVL1:
                mensaje_victoria = fuente_victoria.render("¡VICTORIA! Enter para volver a jugar!", True, AMARILLO)
                self.pantalla.blit(mensaje_victoria, (ANCHO_PANTALLA // 2 - mensaje_victoria.get_width() // 2,
                                                      ALTO_PANTALLA // 2 - mensaje_victoria.get_height() // 2))

                # Pausar el juego hasta que el jugador presione una tecla para volver al menú
                pygame.display.flip()
                self.espera_enter()
                self.menu.ejecutar_menu()  # Volver al menú si el jugador muere
                self.ejecutar = False
                break

            # Colisiones de rect jugador y enemigos:
            for enemigo in self.enemigos:

                # Si nuestro personaje golpea al enemigo con el rect_ataque le hace daño:
                if self.personaje.ataque_rect is not None  and self.personaje.rect is not None :
                    if self.personaje.ataque_rect.colliderect(enemigo.rect):
                        muerto = enemigo.quitar_vida(5)

                        # Segun enemigo muertos, sumara los puntos correspondientes:
                        if muerto:
                            if isinstance(enemigo, Enemigo1):
                                self.contador_Puntos += 10
                            elif isinstance(enemigo, Enemigo2):
                                self.contador_Puntos += 15
                            elif isinstance(enemigo, Enemigo3):
                                self.contador_Puntos += 5

                # Si enemigo nos golpea con su ataque nos quitara 25 puntos de vida, si nos toca con el rect del cuerpo, no quitara 5 puntos:
                if  enemigo.rect is not None:
                    muerte = False
                    # Segun con que golpee jugador, hara un daño u otro:
                    if enemigo.ataque_rect.colliderect(self.personaje.rect):
                        muerte = self.personaje.danio_jugador(25)
                    elif enemigo.rect.colliderect(self.personaje.rect):
                        muerte = self.personaje.danio_jugador(5)

                    # Si despues de recibir daño jugador muere, ejecuta evento de muerte:
                    if muerte:
                        self.mostrar_game_over()
                        pygame.mixer.music.load(SONIDO_MENU)
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                        self.menu.ejecutar_menu()  # Volver al menú si el jugador muere
                        self.ejecutar = False
                        break

            pygame.display.flip()

        pygame.quit()


    # Utilizamos este metodo para esperar que el juegador pulse enter para empezar otra partida:
    def espera_enter(self):
        # Esperamos que el jugador presione una tecla para regresar al menú
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    esperando = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:  # Si el jugador presiona Enter, volvemos al menú
                    esperando = False
                    break

    # Utilizamos este metodo para mostrar GAMEOVER y volver a Menu tras una pausa de 2 segundos:
    def mostrar_game_over(self):
        # Mostrar una pantalla de Game Over antes de salir
        fuente_game_over = pygame.font.SysFont("Arial", 60)
        game_over_texto = fuente_game_over.render("GAME OVER", True, ROJO)
        # Dibujamos la frase de GameOver en el centro de la pantalla:
        self.pantalla.blit(game_over_texto, (ANCHO_PANTALLA // 2 - game_over_texto.get_width() // 2,
                                             ALTO_PANTALLA // 2 - game_over_texto.get_height() // 2))
        pygame.display.flip()
        # Pausa de dos segundos:
        pygame.time.wait(2000)
