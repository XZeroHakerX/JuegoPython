import pygame
from Constantes import *
import random

from EnemigoBase import EnemigoBase

# Enemigo 1 tiene velocidad y tiempo ataque aleatorios, pero cuando se instancia el enemigo, no varian:
class Enemigo1(EnemigoBase):

    def __init__(self):
        super().__init__(POSICION_INICIAL_X_ENEMIGO1, POSICION_INICIAL_Y_ENEMIGO1 + random.randrange(-65, 35), ANCHO_ENEMIGO1, ALTURA_ENEMIGO1, POSICION_INICIAL_X_ENEMIGO1 + CENTRO_X_CUADRADO_E1,
                         POSICION_INICIAL_Y_ENEMIGO1 + CENTRO_Y_CUADRADO_E1, VELOCIDAD_ENEMIGO1 + random.randrange(10,30), random.choice([0.02,0.04,0.06,0.08]), VIDA_ENEMIGO1)

        # Cargamos las animaciones correspondientes al enemigo1:
        self.cargar_animaciones(
            caminar=[f"imagenes/enemigo2/andar/e2_andar{i + 1}.png" for i in range(8)],
            atacar=[f"imagenes/enemigo2/ataque/e2_ataque{i + 1}.png" for i in range(10)]
        )







