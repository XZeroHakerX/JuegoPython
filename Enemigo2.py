import pygame
from Constantes import *
import random

from EnemigoBase import EnemigoBase

# Enemigo 2 tiene velocidad y tiempo ataque aleatorios, pero cuando se instancia el enemigo, no varian:
class Enemigo2(EnemigoBase):

    def __init__(self):
        super().__init__(POSICION_INICIAL_X_ENEMIGO2, POSICION_INICIAL_Y_ENEMIGO2 + random.randrange(-65, 35), ANCHO_ENEMIGO2, ALTURA_ENEMIGO2, POSICION_INICIAL_X_ENEMIGO2 + CENTRO_Y_CUADRADO_E2,
                         POSICION_INICIAL_Y_ENEMIGO2 + CENTRO_Y_CUADRADO_E2, VELOCIDAD_ENEMIGO2 + random.randrange(10, 30), random.choice([0.02, 0.04, 0.06, 0.08]),
                         VIDA_ENEMIGO2)

        # Cargamos las animaciones correspondientes al enemigo1:
        self.cargar_animaciones(
            caminar=[f"imagenes/enemigo2/andar/e2_andar{i+1}.png" for i in range(8)],
            atacar=[f"imagenes/enemigo2/ataque/e2_ataque{i+1}.png" for i in range(10)]
        )







