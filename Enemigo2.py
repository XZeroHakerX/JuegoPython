import pygame
from Constantes import *
import random

from EnemigoBase import EnemigoBase



# Enemigo 2 tiene velocidad y tiempo ataque aleatorios, pero cuando se instancia el enemigo, no varian:

class Enemigo2(EnemigoBase):

    def __init__(self):

        velocidad = VELOCIDAD_ENEMIGO2 + random.randrange(5, 10)
        velocidad_ataque = random.choice([0.02, 0.04, 0.06, 0.08])
        y_aleatorio =  POSICION_INICIAL_Y_ENEMIGO2 + random.randrange(0,100)
        super().__init__(
            POSICION_INICIAL_X_ENEMIGO2,
            y_aleatorio,
            ANCHO_ENEMIGO2,
            ALTURA_ENEMIGO2,
            POSICION_INICIAL_X_ENEMIGO2 + CENTRO_X_CUADRADO_E2,
            y_aleatorio + CENTRO_Y_CUADRADO_E2 ,
            velocidad,
            velocidad_ataque,
            VIDA_ENEMIGO2,
            OFFSET_X_RECT_ATAQUE_E2,
            OFFSET_Y_RECT_ATAQUE_E2,
            ANCHO_RECT_ATAQUE_E2,
            ALTO_RECT_ATAQUE_E2

        )

        # Cargamos las animaciones correspondientes al enemigo1:
        self.cargar_animaciones(
            caminar=[f"imagenes/enemigo2/Andar/e2_andar{i+1}.png" for i in range(8)],
            atacar=[f"imagenes/enemigo2/Ataque/e2_ataque{i+1}.png" for i in range(10)],
            danio=[f"imagenes/enemigo2/danio/e2_danio{i+1}.png" for i in range(10)],
            morir=[f"imagenes/enemigo2/morir/e2_morir{i+1}.png" for i in range(20)]
        )







