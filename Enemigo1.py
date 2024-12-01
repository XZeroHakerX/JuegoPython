import pygame
from Constantes import *
import random

from EnemigoBase import EnemigoBase

# Enemigo 1 tiene velocidad y tiempo ataque aleatorios, pero cuando se instancia el enemigo, no varian:
class Enemigo1(EnemigoBase):
    def __init__(self, ):
        # Asignamos velocidad y velocidad_ataque con un factor aleatorio:
        velocidad = VELOCIDAD_ENEMIGO1 + random.randrange(6, 15)
        velocidad_ataque = random.choice([0.02, 0.04, 0.06, 0.08])
        # Igual para la posicion y inicial:
        y_aleatorio = POSICION_INICIAL_Y_ENEMIGO1 + random.randrange(0, 100)

        super().__init__(POSICION_INICIAL_X_ENEMIGO1,
                         y_aleatorio,
                         ANCHO_ENEMIGO1,
                         ALTURA_ENEMIGO1,
                         POSICION_INICIAL_X_ENEMIGO1 + CENTRO_X_CUADRADO_E1,
                         y_aleatorio + CENTRO_Y_CUADRADO_E1,
                         velocidad,
                         velocidad_ataque,
                         VIDA_ENEMIGO1,
                         OFFSET_X_RECT_ATAQUE_E1,
                         OFFSET_Y_RECT_ATAQUE_E1,
                         ANCHO_RECT_ATAQUE_E1,
                         ALTO_RECT_ATAQUE_E1
                         )

        # Cargamos las animaciones correspondientes al enemigo1:
        self.cargar_animaciones(
            caminar=[f"imagenes/enemigo1/andar/e1_andar{i + 1}.png" for i in range(6)],
            atacar=[f"imagenes/enemigo1/atacar/e1_atacar{i + 1}.png" for i in range(6)],
            danio=[f"imagenes/enemigo1/danio/e1_danio{i + 1}.png" for i in range(10)],
            morir=[f"imagenes/enemigo1/morir/e1_morir{i + 1}.png" for i in range(20)]
        )







