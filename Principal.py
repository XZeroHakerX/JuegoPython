import pygame, sys
from pygame.locals import *
from Personaje import *

# Inicializamos Pygame
pygame.init()


# Variables de configuración
W, H = 1000, 600
FPS = 18
RELOJ = pygame.time.Clock()

# Configuración de la pantalla
PANTALLA = pygame.display.set_mode((W, H))
pygame.display.set_caption("Adventure P-ychigo")
icono = pygame.image.load("imagenes/icono.png")
pygame.display.set_icon(icono)

# Fondo del juego
fondo = pygame.image.load("imagenes/background_lvl_1.png")


# Animaciones del personaje
idle = [pygame.image.load(f"imagenes/Idle/Idle{i+1}.png").convert_alpha() for i in range(9)]
saltoAni = [pygame.image.load(f"imagenes/salto{i+1}.png").convert_alpha() for i in range(2)]
caminaderecha = [pygame.image.load(f"imagenes/caminar/andar{i+1}.png").convert_alpha() for i in range(8)]
caminaizquierda = [pygame.image.load(f"imagenes/caminar/andar{i+1}I.png").convert_alpha() for i in range(8)]


personaje = Personaje()
# Variables del personaje
px = 50
py = 450
ancho = 40
velocidad = 10

# Variables de salto
salto = False
alturaSalto = 10


#Musica fondo
#pygame.mixer.music.load("sonidos/sonido_pelea.mp3")
#pygame.mixer.music.play(-1)

# Variables de movimiento
en_idle = True
izquierda = False
derecha = False
arriba = False
abajo = False
cuentapasos = 0

def actualizarPantalla():
    global cuentapasos

    # Dibujar el fondo
    PANTALLA.blit(fondo, (0, 0))

    # Animación del personaje
    if cuentapasos >= 8:
        cuentapasos = 0

    if izquierda and not salto:
        PANTALLA.blit(caminaizquierda[cuentapasos // 1], (int(px), int(py)))
        cuentapasos += 1
    elif derecha and not salto:
        PANTALLA.blit(caminaderecha[cuentapasos // 1], (int(px), int(py)))
        cuentapasos += 1
    elif arriba or abajo:
        if not derecha and not izquierda:
            PANTALLA.blit(caminaderecha[cuentapasos // 1], (int(px), int(py)))
            cuentapasos += 1
    elif salto + 1 >= 2:
        PANTALLA.blit(saltoAni[salto // 1], (int(px), int(py)))
        cuentapasos += 1
    else:  # Animación idle
        PANTALLA.blit(idle[cuentapasos // 1], (int(px), int(py)))
        cuentapasos = (cuentapasos + 1) % len(idle)

    # Actualizar la pantalla
    pygame.display.update()


# Bucle principal del juego
ejecuta = True

while ejecuta:

    RELOJ.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            ejecuta = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and px > velocidad:
        px -= velocidad
        izquierda = True
        derecha = False
        esta_idle = False
    elif keys[pygame.K_d] and px < W - velocidad - ancho:
        px += velocidad
        izquierda = False
        derecha = True
        esta_idle = False
    else:
        esta_idle = True
        izquierda = False
        derecha = False

    if keys[pygame.K_w] and py > 360 and not salto:
        py -= velocidad
        arriba = True
        abajo = False
    elif keys[pygame.K_s] and py < 450 and not salto:
        py += velocidad
        abajo = True
        arriba = False
    else:
        abajo = False
        arriba = False

    if not salto:
        if keys[pygame.K_SPACE]:
            salto = True
            alturaSalto = 10
    else:
        if alturaSalto >= -10:
            py -= (alturaSalto * abs(alturaSalto)) * 0.5
            alturaSalto -= 1
        else:
            salto = False
            alturaSalto = 10

    #if keys[pygame.K_9] and pygame.mixer.music.get_volume() > 0.0:
        #pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.10)


    #if keys[pygame.K_0] and pygame.mixer.music.get_volume() < 1.0:
        #pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.10)

    # Actualizar la pantalla
    actualizarPantalla()

pygame.quit()