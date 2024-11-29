import pygame
from Constantes import *
from Principal import *

if __name__ == "__main__":
    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption(NOMBRE_JUEGO)
    fondo = pygame.image.load(FONDO_JUEGO_MENU)
    RELOJ = pygame.time.Clock()
    ejecutar = True
    animacionStart = [pygame.image.load(f"imagenes/AnimacionMenu/press{i + 1}.png").convert_alpha() for i in range(61)]
    contador = 0

    pygame.mixer.music.load(SONIDO_MENU)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    canal0 = pygame.mixer.Channel(0)
    sonido_2 = pygame.mixer.Sound(SONIDO_MENU_2)
    sonido_2.set_volume(0.6)


    while ejecutar:
        RELOJ.tick(FPS_MENU)

        for event in pygame.event.get():
            if event.type == QUIT:
                ejecutar = False


        pantalla.blit(fondo, (0, 0))

        if(contador == 59):
            if not canal0.get_busy():
                canal0.play(sonido_2)

        if contador >= 61:
           contador = 0
        pantalla.blit(animacionStart[contador // 1], (0, 0))

        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            juego = Principal()
            juego.ejecutar()

        if key[pygame.K_ESCAPE]:
            ejecutar = False

        contador += 1
        pygame.display.flip()

pygame.quit()