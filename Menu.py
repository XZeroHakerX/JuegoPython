import pygame
from Constantes import *
from Lvl1 import Lvl1

# Clase Menu.
# Ejecutamos despues de definir la clase.
class Menu:
    def __init__ (self):
        pygame.init()

        #Configuracion de la pantalla:
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption(NOMBRE_JUEGO)

        # Inicializacion de los recursos:
        # Damos el fondo, la animacion de menu, sonido que se repite en el bucle
        # y cancion de fondo.
        self.fondo = pygame.image.load(FONDO_JUEGO_MENU)
        self.animacionStart = [pygame.image.load(f"imagenes/AnimacionMenu/press{i + 1}.png").convert_alpha() for i in range(61)]
        self.sonido = pygame.mixer.Sound(SONIDO_MENU_2)
        self.sonido.set_volume(0.6)
        pygame.mixer.music.load(SONIDO_MENU)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Canal de sonido:
        # Utilizamos para comprobar que esta libre y no hay sonido sobrepuestos
        self.canal0 = pygame.mixer.Channel(0)

        # Controladores:
        # Aqui tenemos el reloj, la variable para que se ejecute el bucle, y un
        # contador para hacer el cambio de sprite en la animacion de menu
        self.reloj = pygame.time.Clock()
        self.ejecutar = True



    # Generador para animar el menu de entrada, devuelve el contador
    # con yield y queda a la espera de ser llamado otra vez para devolver
    # contador + 1 o 0 segun si llego o no al limite de imagenes.
    def animacion(self):
        contador = 0
        while True:
            yield contador
            contador += 1
            if contador >= len(self.animacionStart):
                contador = 0


    # Separamos los eventos del usuario como teclado y evento de QUIT para
    # mas claridad en el codigo
    def eventos(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               self. ejecutar = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.ejecutar = False

        if keys[pygame.K_RETURN]:
            pantalla1 = Lvl1()
            pantalla1.ejecutar_lvl1()


    #Metodo para empezar y ejecutar el menu:
    def ejecutarMenu(self):

        # Aqui generamos una sola vez el generador
        animacion = self.animacion()

        while self.ejecutar:

            #Damos los FPS a la pantalla
            self.reloj.tick(FPS_MENU)

            # Ejecutamos los Eventos:
            self.eventos()

            # Ajustar fondo y dibujarlo:
            self.pantalla.blit(self.fondo, (0, 0))

            # Animacion del fondo, a cada ciclo pedimos con next un nuevo indice para el siguiente
            # sprite de la aniamcion y la dibujamos:
            frame = next(animacion)
            self.pantalla.blit(self.animacionStart[frame], (0, 0))

            # Sonido se ejecuta al frame 59 de la animacion:
            if frame == 59 and not self.canal0.get_busy():
                    self.canal0.play(self.sonido)

            # Actualizamos la pantalla completa:
            pygame.display.flip()

    pygame.quit()


#Aqui tenemos la inicializacion del programa, con la llamada al Menu:
if __name__ == "__main__":
    menu = Menu()
    menu.ejecutarMenu()