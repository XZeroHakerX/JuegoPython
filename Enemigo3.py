import pygame
from Constantes import *
import random

from EnemigoBase import EnemigoBase



# Enemigo 2 tiene velocidad y tiempo ataque aleatorios, pero cuando se instancia el enemigo, no varian:

class Enemigo3(EnemigoBase):

    def __init__(self):

        velocidad = VELOCIDAD_ENEMIGO3 + random.randrange(5, 10)
        velocidad_ataque = random.choice([0.02, 0.04, 0.06, 0.08])
        y_aleatorio =  POSICION_INICIAL_Y_ENEMIGO3 + random.randrange(0,150)
        super().__init__(
            POSICION_INICIAL_X_ENEMIGO3,
            y_aleatorio,
            ANCHO_ENEMIGO3,
            ALTURA_ENEMIGO3,
            POSICION_INICIAL_X_ENEMIGO3 + CENTRO_X_CUADRADO_E3,
            y_aleatorio + CENTRO_Y_CUADRADO_E3 ,
            velocidad,
            velocidad_ataque,
            VIDA_ENEMIGO3,
            OFFSET_X_RECT_ATAQUE_E3,
            OFFSET_Y_RECT_ATAQUE_E3,
            ANCHO_RECT_ATAQUE_E3,
            ALTO_RECT_ATAQUE_E3

        )

        # Cargamos las animaciones correspondientes al enemigo1:
        self.cargar_animaciones(
            caminar=[f"imagenes/enemigo3/Andar/e3_andar{i+1}.png" for i in range(8)],
            atacar=[f"imagenes/enemigo3/Atacar/e3_atacar{i+1}.png" for i in range(9)],
            danio=[f"imagenes/enemigo3/danio/e3_danio{i+1}.png" for i in range(10)],
            morir=[f"imagenes/enemigo3/morir/e3_morir{i+1}.png" for i in range(20)]
        )