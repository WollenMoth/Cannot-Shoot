"""Módulo que contiene la clase Block."""

import pygame
from common import Coordinate
from colors import WHITE
from models.ball import Ball

BLOCK_COLOR = WHITE


class Block:
    """Representa un bloque destruible por las bolas."""

    def __init__(self, start: Coordinate, width: int, height: int) -> None:
        """Inicializa los atributos del objeto bloque.

        Args:
            start (Coordinate): Coordenadas (x, y) del punto superior izquierdo del bloque.
            width (int): Ancho del bloque.
        """
        self.start = start
        self.width = width
        self.height = height
        self.color = BLOCK_COLOR

    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja el bloque en la pantalla."""
        rect = (*self.start, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)

    def collide(self, ball: Ball) -> bool:
        """Comprueba si la bola colisiona con el bloque.

        Args:
            ball (Ball): Bola que colisiona con el bloque.

        Returns:
            bool: True si la bola colisiona con el bloque, False en caso contrario.
        """
        return ball.center[1] - ball.radius <= self.start[1] + self.height and \
            ball.center[1] + ball.radius >= self.start[1] and \
            ball.center[0] - ball.radius <= self.start[0] + self.width and \
            ball.center[0] + ball.radius >= self.start[0]
