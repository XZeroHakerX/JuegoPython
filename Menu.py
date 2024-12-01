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

        self.fondo = pygame.image.load(FONDO_JUEGO_MENU)
        self.animacionStart = [pygame.image.load(f"imagenes/AnimacionMenu/press{i + 1}.png").convert_alpha() for i in range(61)]
        self.icono = pygame.image.load(ICONO_JUEGO)
        pygame.display.set_icon(self.icono)

        self.sonido = pygame.mixer.Sound(SONIDO_MENU_2)
        self.sonido.set_volume(0.6)

        pygame.mixer.music.load(SONIDO_MENU)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.canal0 = pygame.mixer.Channel(0)

        self.reloj = pygame.time.Clock()
        self.ejecutar = True

    def animacion(self):
        contador = 0
        while True:
            yield contador
            contador += 1
            if contador >= len(self.animacionStart):
                contador = 0

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ejecutar = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.ejecutar = False

        if keys[pygame.K_RETURN]:
            # Al presionar Enter, comenzamos el nivel 1
            pantalla1 = Lvl1(self)  # Pasamos la referencia del menú al nivel
            pantalla1.ejecutar_lvl1()

    def ejecutar_menu(self):
        animacion = self.animacion()

        while self.ejecutar:
            self.reloj.tick(FPS_MENU)
            self.eventos()

            self.pantalla.blit(self.fondo, (0, 0))
            frame = next(animacion)
            self.pantalla.blit(self.animacionStart[frame], (0, 0))

            if frame == 59 and not self.canal0.get_busy():
                self.canal0.play(self.sonido)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    menu = Menu()
    menu.ejecutar_menu()