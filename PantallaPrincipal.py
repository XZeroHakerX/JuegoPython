import pygame


class PantallaPrincipal:
    def __init__(self):
        self.titulo = "Adventure P-ychigo"

    def manejar_eventos(self, eventos):
        for evento in eventos:
           if evento.type == pygame.KEYDOWN:
               if evento.key == pygame.K_ESCAPE:
                   return "Principal"
        return None

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pantalla.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        texto = font.render(self.titulo, True, (255, 255, 255))
        pantalla.blit(texto, (0, 0))
