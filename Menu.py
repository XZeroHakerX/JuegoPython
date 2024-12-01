import pygame
from Constantes import *
from Lvl1 import *

# Clase Menu.
# Ejecutamos despues de definir la clase.
class Menu:
    def __init__(self):
        pygame.init()

        # Configuración de la pantalla:
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption(NOMBRE_JUEGO)

        # Cargamos los recursos necesarios visuales:
        self.fondo = pygame.image.load(FONDO_JUEGO_MENU)
        self.animacionStart = [pygame.image.load(f"imagenes/AnimacionMenu/press{i + 1}.png").convert_alpha() for i in range(61)]
        self.icono = pygame.image.load(ICONO_JUEGO)
        pygame.display.set_icon(self.icono)

        # Aqui cargamos recursos de audio:
        self.sonido = pygame.mixer.Sound(SONIDO_MENU_2)
        self.sonido.set_volume(0.6)

        # Cargamos y ejecutamos la musica de fondo:
        pygame.mixer.music.load(SONIDO_MENU)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # En bucle para que no se pare la musica.

        # Canal para reproducir los audios:
        self.canal0 = pygame.mixer.Channel(0)

        self.reloj = pygame.time.Clock()
        self.ejecutar = True


    # Generador de animacion del texto de pulsar enter:
    def animacion(self):
        contador = 0
        while True:
            yield contador
            contador += 1
            if contador >= len(self.animacionStart):
                contador = 0

    # Eventos en un metodo aislado:
    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ejecutar = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.ejecutar = False

        if keys[pygame.K_RETURN]:

            # Al presionar Enter, comenzamos el nivel 1
            pantalla1 = Lvl1(self)  # Pasamos la referencia del menu al nivel
            pantalla1.ejecutar_lvl1()

    # Metodo para ejecutar el menu:
    def ejecutar_menu(self):
        animacion = self.animacion()

        while self.ejecutar:
            self.reloj.tick(FPS_MENU)
            self.eventos()

            # Dibujamos la animacion pidiendo el siguiente indice al generador:
            self.pantalla.blit(self.fondo, (0, 0))
            frame = next(animacion)
            self.pantalla.blit(self.animacionStart[frame], (0, 0))

            # Reproducimos un sonido en el fram 59
            if frame == 59 and not self.canal0.get_busy():
                self.canal0.play(self.sonido)

            pygame.display.flip()

        pygame.quit()

# Iniciamos el Menu:
if __name__ == "__main__":
    menu = Menu()
    menu.ejecutar_menu()